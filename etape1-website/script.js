// =============================================
// SCRIPT.JS - Scripts E-commerce
// =============================================

// Attendre que le DOM soit chargé
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 E-commerce scripts chargés');
    
    // Initialiser les fonctionnalités
    initHomePage();
    initProductsPage();
    initCartPage();
    initContactPage();
    initFAQ();
});

// ===== PAGE D'ACCUEIL =====
function initHomePage() {
    // Bouton "Acheter maintenant"
    const shopNowBtn = document.getElementById('btn-shop-now');
    if (shopNowBtn) {
        shopNowBtn.addEventListener('click', () => {
            window.location.href = 'products.html';
            trackEvent('shop_now_clicked', {});
        });
    }

    // Cartes de catégories
    const categoryCards = document.querySelectorAll('.category-card');
    categoryCards.forEach(card => {
        card.addEventListener('click', (e) => {
            const category = e.currentTarget.getAttribute('data-category');
            window.location.href = `products.html?category=${category}`;
            trackEvent('category_clicked', { category: category });
        });
    });

    // Charger les produits en vedette
    const featuredContainer = document.getElementById('featured-products');
    if (featuredContainer) {
        const featured = getFeaturedProducts(4);
        featuredContainer.innerHTML = featured.map(product => createProductCard(product)).join('');
        
        // Ajouter les événements aux boutons
        attachProductCardEvents(featuredContainer);
    }

    // Bouton promo
    const promoBtn = document.getElementById('btn-promo');
    if (promoBtn) {
        promoBtn.addEventListener('click', () => {
            window.location.href = 'products.html?category=laptops';
            trackEvent('promo_banner_clicked', {});
        });
    }

    // Formulaire newsletter
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const email = document.getElementById('input-email').value;
            const messageDiv = document.getElementById('form-message');

            setTimeout(() => {
                messageDiv.textContent = `✅ Merci ! Vous recevrez 10% de réduction à ${email}`;
                messageDiv.className = 'message success';
                
                trackEvent('newsletter_signup', {
                    email_domain: email.split('@')[1]
                });

                newsletterForm.reset();

                setTimeout(() => {
                    messageDiv.className = 'message';
                }, 5000);
            }, 500);
        });
    }
}

// Créer une card produit
function createProductCard(product) {
    return `
        <div class="product-card" data-product-id="${product.id}">
            <div class="product-image">${product.image}</div>
            <h3 class="product-name">${product.name}</h3>
            <p class="product-description">${product.description}</p>
            <div class="product-rating">
                ${'⭐'.repeat(Math.floor(product.rating))} ${product.rating}
            </div>
            <div class="product-price">${formatPrice(product.price)}</div>
            <div class="product-stock ${product.stock < 5 ? 'low-stock' : ''}">
                ${product.stock < 5 ? `⚠️ Plus que ${product.stock} en stock` : `✅ ${product.stock} en stock`}
            </div>
            <button class="btn btn-primary btn-add-to-cart" data-product-id="${product.id}">
                🛒 Ajouter au panier
            </button>
        </div>
    `;
}

// Attacher les événements aux cards produits
function attachProductCardEvents(container) {
    const addToCartBtns = container.querySelectorAll('.btn-add-to-cart');
    addToCartBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const productId = parseInt(btn.getAttribute('data-product-id'));
            const product = getProductById(productId);
            
            if (cart.addItem(productId)) {
                showNotification(`✅ ${product.name} ajouté au panier !`, 'success');
            }
        });
    });

    // Clic sur la card pour voir les détails
    const productCards = container.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('click', (e) => {
            if (!e.target.classList.contains('btn-add-to-cart')) {
                const productId = card.getAttribute('data-product-id');
                const product = getProductById(parseInt(productId));
                showProductDetails(product);
                trackEvent('product_viewed', {
                    product_id: productId,
                    product_name: product.name
                });
            }
        });
    });
}

// ===== PAGE PRODUITS =====
function initProductsPage() {
    const productsContainer = document.getElementById('all-products');
    if (!productsContainer) return;

    let currentProducts = getAllProducts();

    // Récupérer la catégorie depuis l'URL
    const urlParams = new URLSearchParams(window.location.search);
    const categoryParam = urlParams.get('category');
    if (categoryParam) {
        document.getElementById('filter-category').value = categoryParam;
    }

    // Fonction pour afficher les produits
    function displayProducts() {
        const category = document.getElementById('filter-category').value;
        const priceRange = document.getElementById('filter-price').value;
        const sortBy = document.getElementById('filter-sort').value;

        let filtered = getProductsByCategory(category);
        filtered = filterByPrice(filtered, priceRange);
        filtered = sortProducts(filtered, sortBy);

        if (filtered.length === 0) {
            productsContainer.innerHTML = '';
            document.getElementById('no-results').style.display = 'block';
        } else {
            productsContainer.innerHTML = filtered.map(product => createProductCard(product)).join('');
            document.getElementById('no-results').style.display = 'none';
            attachProductCardEvents(productsContainer);
        }

        trackEvent('products_filtered', {
            category: category,
            price_range: priceRange,
            sort: sortBy,
            results_count: filtered.length
        });
    }

    // Événements des filtres
    document.getElementById('filter-category').addEventListener('change', displayProducts);
    document.getElementById('filter-price').addEventListener('change', displayProducts);
    document.getElementById('filter-sort').addEventListener('change', displayProducts);

    // Affichage initial
    displayProducts();
}

// ===== PAGE PANIER =====
function initCartPage() {
    const cartContainer = document.getElementById('cart-items-container');
    if (!cartContainer) return;

    function displayCart() {
        const items = cart.getItems();

        if (items.length === 0) {
            document.getElementById('cart-items-container').innerHTML = '';
            document.getElementById('empty-cart').style.display = 'block';
            document.getElementById('cart-summary-container').style.display = 'none';
        } else {
            document.getElementById('empty-cart').style.display = 'none';
            document.getElementById('cart-summary-container').style.display = 'block';

            cartContainer.innerHTML = items.map(item => `
                <div class="cart-item" data-product-id="${item.productId}">
                    <div class="cart-item-image">${item.product.image}</div>
                    <div class="cart-item-details">
                        <h3>${item.product.name}</h3>
                        <p>${item.product.description}</p>
                        <div class="cart-item-price">${formatPrice(item.product.price)}</div>
                    </div>
                    <div class="cart-item-quantity">
                        <button class="btn-quantity" data-action="decrease" data-product-id="${item.productId}">-</button>
                        <input type="number" class="quantity-input" value="${item.quantity}" min="1" data-product-id="${item.productId}">
                        <button class="btn-quantity" data-action="increase" data-product-id="${item.productId}">+</button>
                    </div>
                    <div class="cart-item-subtotal">${formatPrice(item.subtotal)}</div>
                    <button class="btn-remove" data-product-id="${item.productId}">🗑️</button>
                </div>
            `).join('');

            // Mettre à jour le résumé
            document.getElementById('cart-subtotal').textContent = formatPrice(cart.getSubtotal());
            document.getElementById('cart-shipping').textContent = cart.getShipping() === 0 ? 'Gratuite' : formatPrice(cart.getShipping());
            document.getElementById('cart-tax').textContent = formatPrice(cart.getTax());
            document.getElementById('cart-total').textContent = formatPrice(cart.getTotal());

            // Événements
            attachCartEvents();
        }
    }

    function attachCartEvents() {
        // Boutons de quantité
        document.querySelectorAll('.btn-quantity').forEach(btn => {
            btn.addEventListener('click', () => {
                const productId = parseInt(btn.getAttribute('data-product-id'));
                const action = btn.getAttribute('data-action');
                const item = cart.items.find(i => i.productId === productId);
                
                if (action === 'increase') {
                    cart.updateQuantity(productId, item.quantity + 1);
                } else if (action === 'decrease' && item.quantity > 1) {
                    cart.updateQuantity(productId, item.quantity - 1);
                }
                
                displayCart();
            });
        });

        // Inputs de quantité
        document.querySelectorAll('.quantity-input').forEach(input => {
            input.addEventListener('change', () => {
                const productId = parseInt(input.getAttribute('data-product-id'));
                const quantity = parseInt(input.value);
                cart.updateQuantity(productId, quantity);
                displayCart();
            });
        });

        // Boutons de suppression
        document.querySelectorAll('.btn-remove').forEach(btn => {
            btn.addEventListener('click', () => {
                const productId = parseInt(btn.getAttribute('data-product-id'));
                const product = getProductById(productId);
                if (confirm(`Supprimer ${product.name} du panier ?`)) {
                    cart.removeItem(productId);
                    displayCart();
                    showNotification('Produit retiré du panier', 'info');
                }
            });
        });
    }

    // Bouton checkout
    const checkoutBtn = document.getElementById('btn-checkout');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', () => {
            if (cart.getTotalItems() > 0) {
                document.getElementById('checkout-modal').style.display = 'block';
                trackEvent('checkout_started', {
                    items_count: cart.getTotalItems(),
                    total: cart.getTotal()
                });
            } else {
                alert('Votre panier est vide !');
            }
        });
    }

    // Modal checkout
    const modal = document.getElementById('checkout-modal');
    const closeBtn = modal?.querySelector('.close');
    
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Formulaire checkout
    const checkoutForm = document.getElementById('checkout-form');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const formData = {
                firstname: document.getElementById('checkout-firstname').value,
                lastname: document.getElementById('checkout-lastname').value,
                email: document.getElementById('checkout-email').value,
                phone: document.getElementById('checkout-phone').value,
                address: document.getElementById('checkout-address').value,
                city: document.getElementById('checkout-city').value,
                zip: document.getElementById('checkout-zip').value,
                payment: document.querySelector('input[name="payment"]:checked').value
            };

            trackEvent('order_completed', {
                ...formData,
                items_count: cart.getTotalItems(),
                total: cart.getTotal(),
                payment_method: formData.payment
            });

            alert(`✅ Commande confirmée !\n\nMerci ${formData.firstname} ${formData.lastname} !\nVous recevrez une confirmation à ${formData.email}\n\nTotal: ${formatPrice(cart.getTotal())}`);
            
            cart.clear();
            modal.style.display = 'none';
            window.location.href = 'index.html';
        });
    }

    // Code promo
    const applyPromoBtn = document.getElementById('btn-apply-promo');
    if (applyPromoBtn) {
        applyPromoBtn.addEventListener('click', () => {
            const code = document.getElementById('promo-code').value;
            const messageDiv = document.getElementById('promo-message');
            
            const promo = cart.applyPromoCode(code);
            
            if (promo) {
                messageDiv.textContent = `✅ Code promo appliqué : ${promo.description}`;
                messageDiv.className = 'message success';
            } else {
                messageDiv.textContent = '❌ Code promo invalide';
                messageDiv.className = 'message error';
            }

            setTimeout(() => {
                messageDiv.className = 'message';
            }, 3000);
        });
    }

    // Affichage initial
    displayCart();
}

// ===== PAGE DE CONTACT =====
function initContactPage() {
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const name = document.getElementById('contact-name').value;
            const email = document.getElementById('contact-email').value;
            const subject = document.getElementById('contact-subject').value;
            const message = document.getElementById('contact-message').value;
            const newsletter = document.getElementById('contact-newsletter')?.checked || false;
            const messageDiv = document.getElementById('contact-message');

            // Validation simple
            if (!name || !email || !subject || !message) {
                if (messageDiv) {
                    messageDiv.textContent = '❌ Veuillez remplir tous les champs obligatoires';
                    messageDiv.className = 'message error';
                }
                return;
            }

            // Simuler l'envoi
            setTimeout(() => {
                if (messageDiv) {
                    messageDiv.textContent = `✅ Merci ${name} ! Votre message a été envoyé avec succès.`;
                    messageDiv.className = 'message success';
                }
                
                if (window.trackEvent) {
                    trackEvent('contact_form_submit', {
                        subject: subject,
                        message_length: message.length,
                        newsletter_opted: newsletter
                    });
                }

                contactForm.reset();

                setTimeout(() => {
                    if (messageDiv) {
                        messageDiv.className = 'message';
                    }
                }, 5000);
            }, 500);
        });
    }

    // Boutons sociaux
    const socialButtons = document.querySelectorAll('.btn-social');
    socialButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const platform = e.target.getAttribute('data-social');
            alert(`🔗 Redirection vers ${platform}... (Simulé)`);
            if (window.trackEvent) {
                trackEvent('social_link_clicked', { platform: platform });
            }
        });
    });

    // Liens footer
    const footerLinks = ['link-shipping', 'link-returns', 'link-privacy', 'link-terms'];
    footerLinks.forEach(linkId => {
        const link = document.getElementById(linkId);
        if (link) {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                alert(`Information sur: ${linkId.replace('link-', '')}`);
                if (window.trackEvent) {
                    trackEvent('footer_link_clicked', { link: linkId });
                }
            });
        }
    });
}

// ===== FAQ (Accordéon) =====
function initFAQ() {
    const faqQuestions = document.querySelectorAll('.faq-question');
    faqQuestions.forEach(question => {
        question.addEventListener('click', (e) => {
            const faqItem = e.target.closest('.faq-item');
            const wasActive = faqItem.classList.contains('active');
            
            // Fermer tous les autres
            document.querySelectorAll('.faq-item').forEach(item => {
                item.classList.remove('active');
            });
            
            // Ouvrir celui-ci si il était fermé
            if (!wasActive) {
                faqItem.classList.add('active');
                if (window.trackEvent) {
                    trackEvent('faq_opened', { question: question.textContent.substring(0, 50) });
                }
            }
        });
    });
}

// ===== MODAL POUR LES FEATURES =====
function showProductDetails(product) {
    alert(`${product.name}\n\n${product.description}\n\nPrix: ${formatPrice(product.price)}\nStock: ${product.stock}\nNote: ${product.rating}⭐`);
}

// ===== NOTIFICATIONS =====
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// ===== FONCTIONS UTILITAIRES =====

// Détecter l'inactivité
let inactivityTimer;
function resetInactivityTimer() {
    clearTimeout(inactivityTimer);
    inactivityTimer = setTimeout(() => {
        if (window.trackEvent) {
            trackEvent('user_inactive', { inactive_seconds: 60 });
        }
    }, 60000); // 1 minute d'inactivité
}

document.addEventListener('mousemove', resetInactivityTimer);
document.addEventListener('keypress', resetInactivityTimer);
document.addEventListener('click', resetInactivityTimer);
resetInactivityTimer();

// Détecter la visibilité de la page
document.addEventListener('visibilitychange', () => {
    if (window.trackEvent) {
        if (document.hidden) {
            trackEvent('page_hidden', {});
        } else {
            trackEvent('page_visible', {});
        }
    }
});

// Performance : mesurer le temps de chargement
window.addEventListener('load', () => {
    setTimeout(() => {
        const perfData = window.performance.timing;
        const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
        const domReadyTime = perfData.domContentLoadedEventEnd - perfData.navigationStart;
        
        if (window.trackEvent) {
            trackEvent('performance_metrics', {
                page_load_time_ms: pageLoadTime,
                dom_ready_time_ms: domReadyTime,
                dns_time_ms: perfData.domainLookupEnd - perfData.domainLookupStart,
                tcp_time_ms: perfData.connectEnd - perfData.connectStart
            });
        }
    }, 0);
});

console.log('✨ Scripts E-commerce activés - Tous les événements sont trackés !');
