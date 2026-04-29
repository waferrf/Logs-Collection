// =============================================
// BASE DE DONNÉES DES PRODUITS
// =============================================

const PRODUCTS = [
    // SMARTPHONES
    {
        id: 1,
        name: "iPhone 15 Pro",
        category: "smartphones",
        price: 1299,
        image: "📱",
        description: "Le dernier iPhone avec puce A17 Pro et caméra 48MP",
        stock: 15,
        rating: 4.8
    },
    {
        id: 2,
        name: "Samsung Galaxy S24",
        category: "smartphones",
        price: 999,
        image: "📱",
        description: "Smartphone Android haut de gamme avec écran AMOLED",
        stock: 20,
        rating: 4.6
    },
    {
        id: 3,
        name: "Google Pixel 8",
        category: "smartphones",
        price: 799,
        image: "📱",
        description: "Meilleur appareil photo sur smartphone avec IA Google",
        stock: 12,
        rating: 4.7
    },
    {
        id: 4,
        name: "OnePlus 12",
        category: "smartphones",
        price: 699,
        image: "📱",
        description: "Performance exceptionnelle à prix compétitif",
        stock: 8,
        rating: 4.5
    },

    // ORDINATEURS PORTABLES
    {
        id: 5,
        name: "MacBook Pro 16\"",
        category: "laptops",
        price: 2799,
        image: "💻",
        description: "Puissance M3 Max pour les professionnels",
        stock: 5,
        rating: 4.9
    },
    {
        id: 6,
        name: "Dell XPS 15",
        category: "laptops",
        price: 1899,
        image: "💻",
        description: "PC portable premium avec écran OLED 4K",
        stock: 10,
        rating: 4.7
    },
    {
        id: 7,
        name: "Lenovo ThinkPad X1",
        category: "laptops",
        price: 1599,
        image: "💻",
        description: "Laptop professionnel robuste et fiable",
        stock: 7,
        rating: 4.6
    },
    {
        id: 8,
        name: "ASUS ROG Zephyrus",
        category: "laptops",
        price: 2199,
        image: "💻",
        description: "PC gaming portable avec RTX 4080",
        stock: 6,
        rating: 4.8
    },
    {
        id: 9,
        name: "HP Pavilion",
        category: "laptops",
        price: 899,
        image: "💻",
        description: "Ordinateur portable polyvalent pour tous les jours",
        stock: 15,
        rating: 4.3
    },

    // ACCESSOIRES
    {
        id: 10,
        name: "AirPods Pro",
        category: "accessories",
        price: 279,
        image: "🎧",
        description: "Écouteurs sans fil avec réduction de bruit active",
        stock: 25,
        rating: 4.7
    },
    {
        id: 11,
        name: "Sony WH-1000XM5",
        category: "accessories",
        price: 399,
        image: "🎧",
        description: "Meilleur casque antibruit du marché",
        stock: 12,
        rating: 4.9
    },
    {
        id: 12,
        name: "Logitech MX Master 3",
        category: "accessories",
        price: 109,
        image: "🖱️",
        description: "Souris ergonomique pour productivité maximale",
        stock: 30,
        rating: 4.8
    },
    {
        id: 13,
        name: "Apple Magic Keyboard",
        category: "accessories",
        price: 149,
        image: "⌨️",
        description: "Clavier sans fil élégant et confortable",
        stock: 18,
        rating: 4.5
    },
    {
        id: 14,
        name: "Anker PowerBank 20000mAh",
        category: "accessories",
        price: 45,
        image: "🔋",
        description: "Batterie externe haute capacité",
        stock: 40,
        rating: 4.6
    },
    {
        id: 15,
        name: "SanDisk SSD 1TB",
        category: "accessories",
        price: 129,
        image: "💾",
        description: "Disque dur externe ultra rapide",
        stock: 22,
        rating: 4.7
    },

    // TABLETTES
    {
        id: 16,
        name: "iPad Pro 12.9\"",
        category: "tablets",
        price: 1299,
        image: "📲",
        description: "Tablette professionnelle avec puce M2",
        stock: 8,
        rating: 4.8
    },
    {
        id: 17,
        name: "Samsung Galaxy Tab S9",
        category: "tablets",
        price: 899,
        image: "📲",
        description: "Tablette Android premium avec S Pen inclus",
        stock: 12,
        rating: 4.6
    },
    {
        id: 18,
        name: "iPad Air",
        category: "tablets",
        price: 699,
        image: "📲",
        description: "Tablette légère et puissante pour tous les usages",
        stock: 15,
        rating: 4.7
    },
    {
        id: 19,
        name: "Microsoft Surface Pro 9",
        category: "tablets",
        price: 1099,
        image: "📲",
        description: "Tablette 2-en-1 avec Windows 11",
        stock: 6,
        rating: 4.5
    },
    {
        id: 20,
        name: "Amazon Fire HD 10",
        category: "tablets",
        price: 149,
        image: "📲",
        description: "Tablette économique pour le divertissement",
        stock: 25,
        rating: 4.2
    }
];

// Fonction pour obtenir tous les produits
function getAllProducts() {
    return PRODUCTS;
}

// Fonction pour obtenir un produit par ID
function getProductById(id) {
    return PRODUCTS.find(p => p.id === parseInt(id));
}

// Fonction pour obtenir les produits par catégorie
function getProductsByCategory(category) {
    if (category === 'all') return PRODUCTS;
    return PRODUCTS.filter(p => p.category === category);
}

// Fonction pour filtrer par prix
function filterByPrice(products, priceRange) {
    if (priceRange === 'all') return products;
    
    const [min, max] = priceRange.split('-').map(p => p.replace('+', ''));
    
    return products.filter(p => {
        if (max) {
            return p.price >= parseInt(min) && p.price <= parseInt(max);
        } else {
            return p.price >= parseInt(min);
        }
    });
}

// Fonction pour trier les produits
function sortProducts(products, sortBy) {
    const sorted = [...products];
    
    switch(sortBy) {
        case 'price-asc':
            return sorted.sort((a, b) => a.price - b.price);
        case 'price-desc':
            return sorted.sort((a, b) => b.price - a.price);
        case 'name':
            return sorted.sort((a, b) => a.name.localeCompare(b.name));
        default:
            return sorted;
    }
}

// Fonction pour obtenir les produits en vedette
function getFeaturedProducts(count = 4) {
    return PRODUCTS
        .filter(p => p.rating >= 4.6)
        .sort((a, b) => b.rating - a.rating)
        .slice(0, count);
}

// Fonction pour formater le prix
function formatPrice(price) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(price);
}
