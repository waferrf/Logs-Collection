// =============================================
// GESTION DU PANIER
// =============================================

class ShoppingCart {
    constructor() {
        this.items = this.loadCart();
        this.updateCartCount();
    }

    // Charger le panier depuis localStorage
    loadCart() {
        const saved = localStorage.getItem('shopping_cart');
        return saved ? JSON.parse(saved) : [];
    }

    // Sauvegarder le panier dans localStorage
    saveCart() {
        localStorage.setItem('shopping_cart', JSON.stringify(this.items));
        this.updateCartCount();
    }

    // Ajouter un produit au panier
    addItem(productId, quantity = 1) {
        const product = getProductById(productId);
        if (!product) return false;

        const existingItem = this.items.find(item => item.productId === productId);

        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            this.items.push({
                productId: productId,
                quantity: quantity,
                addedAt: new Date().toISOString()
            });
        }

        this.saveCart();
        
        // Tracker l'événement
        if (window.trackEvent) {
            trackEvent('add_to_cart', {
                product_id: productId,
                product_name: product.name,
                product_price: product.price,
                quantity: quantity
            });
        }

        return true;
    }

    // Retirer un produit du panier
    removeItem(productId) {
        const index = this.items.findIndex(item => item.productId === productId);
        if (index > -1) {
            const product = getProductById(productId);
            this.items.splice(index, 1);
            this.saveCart();

            // Tracker l'événement
            if (window.trackEvent) {
                trackEvent('remove_from_cart', {
                    product_id: productId,
                    product_name: product?.name
                });
            }
        }
    }

    // Mettre à jour la quantité
    updateQuantity(productId, quantity) {
        const item = this.items.find(item => item.productId === productId);
        if (item) {
            item.quantity = Math.max(1, quantity);
            this.saveCart();
        }
    }

    // Vider le panier
    clear() {
        this.items = [];
        this.saveCart();
        
        if (window.trackEvent) {
            trackEvent('clear_cart', {});
        }
    }

    // Obtenir tous les articles avec leurs détails
    getItems() {
        return this.items.map(item => {
            const product = getProductById(item.productId);
            return {
                ...item,
                product: product,
                subtotal: product ? product.price * item.quantity : 0
            };
        }).filter(item => item.product); // Filtrer les produits qui n'existent plus
    }

    // Obtenir le nombre total d'articles
    getTotalItems() {
        return this.items.reduce((total, item) => total + item.quantity, 0);
    }

    // Obtenir le sous-total
    getSubtotal() {
        return this.getItems().reduce((total, item) => total + item.subtotal, 0);
    }

    // Obtenir les frais de livraison
    getShipping() {
        const subtotal = this.getSubtotal();
        return subtotal >= 50 ? 0 : 5.99; // Livraison gratuite à partir de 50€
    }

    // Obtenir la TVA (20%)
    getTax() {
        return this.getSubtotal() * 0.20;
    }

    // Obtenir le total
    getTotal() {
        return this.getSubtotal() + this.getShipping() + this.getTax();
    }

    // Mettre à jour le badge du panier dans la navigation
    updateCartCount() {
        const badges = document.querySelectorAll('#cart-count');
        const count = this.getTotalItems();
        badges.forEach(badge => {
            badge.textContent = count;
            badge.style.display = count > 0 ? 'inline-block' : 'none';
        });
    }

    // Appliquer un code promo
    applyPromoCode(code) {
        const promoCodes = {
            'WELCOME10': { discount: 0.10, description: '10% de réduction' },
            'SAVE20': { discount: 0.20, description: '20% de réduction' },
            'TECHSHOP': { discount: 0.15, description: '15% de réduction' }
        };

        const promo = promoCodes[code.toUpperCase()];
        
        if (promo) {
            if (window.trackEvent) {
                trackEvent('promo_code_applied', {
                    code: code,
                    discount: promo.discount
                });
            }
            return promo;
        }
        
        return null;
    }
}

// Initialiser le panier global
window.cart = new ShoppingCart();
