// =============================================
// TRACKER.JS - Système de tracking d'événements
// =============================================

class EventTracker {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.serverUrl = 'http://localhost:5000/log';
        this.events = [];
        this.pageLoadTime = new Date();
        
        // Initialiser le tracking automatique
        this.init();
    }

    // Générer un ID de session unique
    generateSessionId() {
        const stored = sessionStorage.getItem('session_id');
        if (stored) return stored;
        
        const sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        sessionStorage.setItem('session_id', sessionId);
        return sessionId;
    }

    // Initialiser tous les trackers
    init() {
        this.trackPageView();
        this.trackClicks();
        this.trackScrolling();
        this.trackTimeOnPage();
        this.trackFormInteractions();
        this.trackMouseMovement();
        
        console.log('🔍 Event Tracker initialisé - Session:', this.sessionId);
    }

    // Méthode générique pour envoyer un événement
    async sendEvent(eventType, eventData = {}) {
        const event = {
            timestamp: new Date().toISOString(),
            event_type: eventType,
            session_id: this.sessionId,
            page_url: window.location.pathname,
            page_title: document.title,
            referrer: document.referrer,
            user_agent: navigator.userAgent,
            screen_width: window.screen.width,
            screen_height: window.screen.height,
            viewport_width: window.innerWidth,
            viewport_height: window.innerHeight,
            ...eventData
        };

        // Stocker localement
        this.events.push(event);

        // ============================================================
        // PILIER 1 : COLLECTE PARALLÈLE — Envoyer aussi à Google Analytics
        // Les deux signaux partent en même temps :
        //   1. Vers notre serveur local (fetch ci-dessous)
        //   2. Vers Google Analytics (gtag ci-dessous)
        // ============================================================
        this.sendToGoogleAnalytics(eventType, eventData);

        // Envoyer au serveur local
        try {
            const response = await fetch(this.serverUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(event)
            });

            if (response.ok) {
                console.log('✅ Événement envoyé:', eventType, eventData);
            } else {
                console.warn('⚠️ Erreur serveur:', response.status);
            }
        } catch (error) {
            console.warn('⚠️ Impossible d\'envoyer au serveur:', error.message);
            // Sauvegarder en localStorage comme fallback
            this.saveToLocalStorage(event);
        }
    }

    // ============================================================
    // ENVOI PARALLÈLE À GOOGLE ANALYTICS (gtag.js)
    // Chaque événement capté par tracker.js est aussi envoyé à GA4
    // via gtag('event', ...) pour permettre la comparaison
    // ============================================================
    sendToGoogleAnalytics(eventType, eventData) {
        // Vérifier que gtag est disponible (le script GA4 est chargé)
        if (typeof gtag !== 'function') {
            console.warn('⚠️ gtag non disponible — événement GA non envoyé');
            return;
        }

        // Mapper les événements locaux vers des événements GA4
        const gaEventMap = {
            'page_view':          'page_view',
            'click':              'clic_tracker',
            'scroll':             'scroll_tracker',
            'time_on_page':       'temps_page_tracker',
            'page_exit':          'sortie_page_tracker',
            'form_submit':        'soumission_formulaire_tracker',
            'form_field_focus':   'focus_champ_tracker',
            'mouse_activity':     'activite_souris_tracker',
            'custom_add_to_cart': 'ajout_panier_tracker',
            'custom_remove_from_cart': 'retrait_panier_tracker',
            'custom_checkout_started': 'debut_paiement_tracker',
            'custom_order_completed':  'commande_terminee_tracker',
            'custom_products_filtered': 'filtre_produits_tracker'
        };

        const gaEventName = gaEventMap[eventType] || eventType.replace('custom_', '') + '_tracker';

        // Préparer les paramètres GA4 (max 25 params, valeurs str max 100 chars)
        const gaParams = {
            tracker_session_id: this.sessionId,
            tracker_page: window.location.pathname,
            tracker_source: 'tracker_js'
        };

        // Ajouter les données pertinentes selon le type
        if (eventData.element_text) {
            gaParams.element_text = String(eventData.element_text).substring(0, 100);
        }
        if (eventData.element_tag) {
            gaParams.element_tag = eventData.element_tag;
        }
        if (eventData.element_id) {
            gaParams.element_id = eventData.element_id;
        }
        if (eventData.scroll_percent !== undefined) {
            gaParams.scroll_percent = eventData.scroll_percent;
        }
        if (eventData.seconds !== undefined) {
            gaParams.time_seconds = eventData.seconds;
        }
        if (eventData.product_name) {
            gaParams.product_name = String(eventData.product_name).substring(0, 100);
        }
        if (eventData.product_price !== undefined) {
            gaParams.product_price = eventData.product_price;
        }
        if (eventData.total_amount !== undefined) {
            gaParams.order_total = eventData.total_amount;
        }

        // Envoyer à Google Analytics en parallèle
        try {
            gtag('event', gaEventName, gaParams);
            console.log('📈 GA4 événement envoyé:', gaEventName);
        } catch (e) {
            console.warn('⚠️ Erreur envoi GA4:', e.message);
        }
    }

    // Sauvegarder en localStorage si le serveur est indisponible
    saveToLocalStorage(event) {
        const stored = JSON.parse(localStorage.getItem('pending_events') || '[]');
        stored.push(event);
        localStorage.setItem('pending_events', JSON.stringify(stored));
    }

    // 1. Tracking de la vue de page
    trackPageView() {
        this.sendEvent('page_view', {
            load_time: new Date() - this.pageLoadTime
        });
    }

    // 2. Tracking des clics
    trackClicks() {
        document.addEventListener('click', (e) => {
            const element = e.target;
            const eventData = {
                element_tag: element.tagName,
                element_id: element.id || null,
                element_class: element.className || null,
                element_text: element.textContent?.substring(0, 100) || null,
                x_position: e.clientX,
                y_position: e.clientY,
                page_x: e.pageX,
                page_y: e.pageY
            };

            // Si c'est un lien
            if (element.tagName === 'A') {
                eventData.link_href = element.href;
                eventData.link_target = element.target;
            }

            // Si c'est un bouton
            if (element.tagName === 'BUTTON' || element.type === 'button' || element.type === 'submit') {
                eventData.button_type = element.type;
                eventData.button_name = element.name;
            }

            this.sendEvent('click', eventData);
        });
    }

    // 3. Tracking du défilement (scroll)
    trackScrolling() {
        let scrollTimeout;
        let maxScroll = 0;

        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            
            const scrollPercent = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
            
            if (scrollPercent > maxScroll) {
                maxScroll = scrollPercent;
            }

            scrollTimeout = setTimeout(() => {
                this.sendEvent('scroll', {
                    scroll_y: window.scrollY,
                    scroll_percent: Math.round(scrollPercent),
                    max_scroll_percent: Math.round(maxScroll)
                });
            }, 500); // Attendre 500ms après le dernier scroll
        });
    }

    // 4. Tracking du temps passé sur la page
    trackTimeOnPage() {
        // Envoyer un événement toutes les 30 secondes
        setInterval(() => {
            const timeOnPage = Math.round((new Date() - this.pageLoadTime) / 1000);
            this.sendEvent('time_on_page', {
                seconds: timeOnPage
            });
        }, 30000);

        // Envoyer lors de la fermeture/navigation
        window.addEventListener('beforeunload', () => {
            const timeOnPage = Math.round((new Date() - this.pageLoadTime) / 1000);
            this.sendEvent('page_exit', {
                time_spent_seconds: timeOnPage
            });
        });
    }

    // 5. Tracking des interactions avec les formulaires
    trackFormInteractions() {
        // Tracking des soumissions de formulaires
        document.addEventListener('submit', (e) => {
            const form = e.target;
            const formData = new FormData(form);
            const fields = {};

            // Collecter les noms des champs (pas les valeurs pour la vie privée)
            for (let [key, value] of formData.entries()) {
                fields[key] = value.length; // Juste la longueur
            }

            this.sendEvent('form_submit', {
                form_id: form.id || null,
                form_action: form.action || null,
                form_method: form.method || null,
                fields_count: Object.keys(fields).length,
                field_names: Object.keys(fields)
            });
        });

        // Tracking des focus sur les champs
        document.addEventListener('focus', (e) => {
            if (e.target.matches('input, textarea, select')) {
                this.sendEvent('form_field_focus', {
                    field_id: e.target.id || null,
                    field_name: e.target.name || null,
                    field_type: e.target.type || null
                });
            }
        }, true);
    }

    // 6. Tracking des mouvements de souris (simplifié)
    trackMouseMovement() {
        let mouseMoveTimeout;
        let moveCount = 0;
        let lastPosition = { x: 0, y: 0 };

        document.addEventListener('mousemove', (e) => {
            moveCount++;
            lastPosition = { x: e.clientX, y: e.clientY };

            clearTimeout(mouseMoveTimeout);
            
            // Envoyer un résumé toutes les 10 secondes
            mouseMoveTimeout = setTimeout(() => {
                if (moveCount > 0) {
                    this.sendEvent('mouse_activity', {
                        move_count: moveCount,
                        last_x: lastPosition.x,
                        last_y: lastPosition.y
                    });
                    moveCount = 0;
                }
            }, 10000);
        });
    }

    // Méthode pour tracker des événements personnalisés
    trackCustomEvent(eventName, eventData = {}) {
        this.sendEvent('custom_' + eventName, eventData);
    }

    // Obtenir tous les événements de la session
    getSessionEvents() {
        return this.events;
    }

    // Obtenir des stats de la session
    getSessionStats() {
        return {
            session_id: this.sessionId,
            total_events: this.events.length,
            session_duration: Math.round((new Date() - this.pageLoadTime) / 1000),
            events_by_type: this.events.reduce((acc, event) => {
                acc[event.event_type] = (acc[event.event_type] || 0) + 1;
                return acc;
            }, {})
        };
    }
}

// Initialiser le tracker automatiquement
window.eventTracker = new EventTracker();

// Exposer des fonctions utiles globalement
window.trackEvent = (eventName, data) => window.eventTracker.trackCustomEvent(eventName, data);
window.getSessionStats = () => window.eventTracker.getSessionStats();

console.log('📊 Tracker chargé. Utilisez trackEvent("nom", {data}) pour des événements personnalisés');
