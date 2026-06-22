<!-- Auditor Dashboard (Final) -->
<!DOCTYPE html>

<html class="dark" lang="es"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Dashboard - Agro-Intelligence Oversight</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Outfit:wght@600;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    "colors": {
                        "outline-variant": "#3f4a3f",
                        "surface-container-low": "#171d17",
                        "primary-container": "#3da35d",
                        "surface-container-lowest": "#0a100a",
                        "on-secondary-fixed-variant": "#1e502e",
                        "inverse-on-surface": "#2c322b",
                        "surface-container": "#1b211b",
                        "surface-variant": "#30362f",
                        "surface-container-highest": "#30362f",
                        "inverse-primary": "#006d33",
                        "primary-fixed": "#92f8a9",
                        "on-surface-variant": "#becabc",
                        "tertiary-fixed-dim": "#89ceff",
                        "on-surface": "#dee4da",
                        "surface-tint": "#76db8f",
                        "tertiary-fixed": "#c9e6ff",
                        "on-error-container": "#ffdad6",
                        "on-tertiary-fixed": "#001e2f",
                        "on-background": "#dee4da",
                        "on-tertiary-fixed-variant": "#004c6e",
                        "error-container": "#93000a",
                        "secondary-container": "#205331",
                        "primary-fixed-dim": "#76db8f",
                        "on-secondary-container": "#8fc599",
                        "on-primary-container": "#003114",
                        "tertiary": "#89ceff",
                        "surface-bright": "#343b34",
                        "secondary": "#9dd3a7",
                        "on-primary-fixed": "#00210b",
                        "on-tertiary": "#00344d",
                        "on-primary": "#003918",
                        "secondary-fixed": "#b8f0c2",
                        "background": "#0f150f",
                        "outline": "#889487",
                        "tertiary-container": "#009ada",
                        "primary": "#76db8f",
                        "on-tertiary-container": "#002d43",
                        "surface-container-high": "#252c25",
                        "surface-dim": "#0f150f",
                        "on-error": "#690005",
                        "inverse-surface": "#dee4da",
                        "surface": "#0f150f",
                        "on-secondary-fixed": "#00210c",
                        "on-primary-fixed-variant": "#005225",
                        "on-secondary": "#01391a",
                        "secondary-fixed-dim": "#9dd3a7",
                        "error": "#ffb4ab"
                    },
                    "borderRadius": {
                        "DEFAULT": "0.125rem",
                        "lg": "0.25rem",
                        "xl": "0.5rem",
                        "full": "0.75rem"
                    },
                    "spacing": {
                        "gutter": "16px",
                        "card-gap": "20px",
                        "container-padding": "24px",
                        "unit": "4px"
                    },
                    "fontFamily": {
                        "body-md": ["Inter"],
                        "headline-sm": ["Outfit"],
                        "body-sm": ["Inter"],
                        "headline-md": ["Outfit"],
                        "display-lg": ["Outfit"],
                        "headline-lg": ["Outfit"],
                        "mono-data": ["monospace"],
                        "label-md": ["Inter"],
                        "body-lg": ["Inter"]
                    },
                    "fontSize": {
                        "body-md": ["16px", { "lineHeight": "24px", "fontWeight": "400" }],
                        "headline-sm": ["20px", { "lineHeight": "28px", "fontWeight": "600" }],
                        "body-sm": ["14px", { "lineHeight": "20px", "fontWeight": "400" }],
                        "headline-md": ["24px", { "lineHeight": "32px", "fontWeight": "600" }],
                        "display-lg": ["48px", { "lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "700" }],
                        "headline-lg": ["32px", { "lineHeight": "40px", "fontWeight": "600" }],
                        "mono-data": ["14px", { "lineHeight": "20px", "fontWeight": "500" }],
                        "label-md": ["12px", { "lineHeight": "16px", "letterSpacing": "0.05em", "fontWeight": "600" }],
                        "body-lg": ["18px", { "lineHeight": "28px", "fontWeight": "400" }]
                    }
                }
            }
        }
    </script>
<style>
        /* Glassmorphism utility classes based on Style Guidance */
        .glass-card {
            background-color: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .glass-panel {
            background-color: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .pulse-border {
            animation: pulse-border 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }

        @keyframes pulse-border {
            0%, 100% { border-color: rgba(255, 180, 171, 0.5); box-shadow: 0 0 0 0 rgba(255, 180, 171, 0.2); }
            50% { border-color: rgba(255, 180, 171, 1); box-shadow: 0 0 10px 2px rgba(255, 180, 171, 0.4); }
        }
        
        /* Custom scrollbar for data tables */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.2);
        }
    </style>
</head>
<body class="bg-background text-on-background font-body-md antialiased min-h-screen overflow-x-hidden selection:bg-primary-container selection:text-on-primary-container">
<!-- TopNavBar (Web) -->
<nav class="hidden md:flex justify-between items-center px-container-padding w-full h-16 bg-surface-container/40 dark:bg-surface-container/40 backdrop-blur-xl docked full-width top-0 border-b border-white/10 shadow-sm z-40 fixed">
<div class="flex items-center gap-6">
<span class="font-headline-md text-headline-md font-bold text-primary tracking-tight">Agro-Intelligence Oversight</span>
<div class="hidden lg:flex items-center gap-1 bg-surface-container-high rounded-full px-4 py-1.5 ml-4 border border-white/5">
<span class="material-symbols-outlined text-primary text-sm mr-2" data-icon="search">search</span>
<input class="bg-transparent border-none text-body-sm text-on-surface focus:ring-0 w-48 placeholder:text-on-surface-variant/50" placeholder="Search parameters, nodes..." type="text"/>
</div>
</div>
<div class="flex items-center gap-8">
<ul class="flex items-center gap-6">
<li class="cursor-pointer active:scale-95 group flex flex-col items-center">
<span class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors py-1">Telemetry</span>
</li>
<li class="cursor-pointer active:scale-95 group flex flex-col items-center">
<span class="font-body-md text-body-md text-primary border-b-2 border-primary pb-1">Audits</span>
</li>
<li class="cursor-pointer active:scale-95 group flex flex-col items-center">
<span class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors py-1">Inventory</span>
</li>
</ul>
<div class="flex items-center gap-4 border-l border-white/10 pl-6">
<button aria-label="Notifications" class="text-on-surface-variant hover:text-primary transition-colors active:scale-95 relative">
<span class="material-symbols-outlined" data-icon="notifications">notifications</span>
<span class="absolute top-0 right-0 w-2 h-2 bg-error rounded-full animate-pulse"></span>
</button>
<button aria-label="Settings" class="text-on-surface-variant hover:text-primary transition-colors active:scale-95">
<span class="material-symbols-outlined" data-icon="settings">settings</span>
</button>
<div class="w-8 h-8 rounded-full bg-surface-container-high border border-primary/30 overflow-hidden ml-2 cursor-pointer">
<img alt="Auditor Profile" class="w-full h-full object-cover" data-alt="A highly detailed professional portrait of an agro-industrial auditor. They are wearing modern, high-tech augmented reality safety glasses over a dark, technical field jacket. The background is a blurred, high-tech precision agriculture monitoring room with subtle green neon lighting and holographic data overlays. The image utilizes a cool, deep charcoal-green cinematic color grading, embodying a clinical, vigilant, and technologically advanced 'Dark-Glassmorphism' visual style." src="https://lh3.googleusercontent.com/aida-public/AB6AXuCxwvAsWimcF03V3njsUr4hg_f38wYuUsLCKv-xiu1PqPz3NR0-RIDqBBNh9BwgAvS4ns7FUNBXzxJ7wtir0npR8M3RPlm_whruKlOLHu7mBAhj9UF9FC6Ux9yZFTa-bKIkz5L2xU5CG3U1ETCNh4zAtHRLCE0utlfji8bJ1Tbf87aVkzvF-PF-2Slr3QZHlE-nDxHkXAMrMMDeWRV6ituElBxadSzZzBDRq378bk6lfFuG5I7oDw0ZHMmUPmTDlExpdWyT9v48Xv4"/>
</div>
</div>
</div>
</nav>
<!-- SideNavBar & Main Content Wrapper -->
<div class="flex h-screen pt-16 md:pt-0">
<!-- SideNavBar (Hidden on Mobile) -->
<aside class="hidden md:flex flex-col py-6 h-full bg-surface-container-lowest dark:bg-surface-container-lowest h-screen w-20 hover:w-64 transition-all duration-300 ease-in-out fixed left-0 top-0 z-50 border-r border-white/5 shadow-2xl group overflow-hidden">
<!-- Header -->
<div class="flex items-center px-4 mb-8 whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300">
<div class="w-10 h-10 rounded-lg bg-surface-container-high flex items-center justify-center border border-white/10 shrink-0">
<span class="material-symbols-outlined text-primary" data-icon="terminal">terminal</span>
</div>
<div class="ml-3">
<div class="font-headline-sm text-headline-sm text-primary-fixed leading-tight">AUDIT_OS_V1</div>
<div class="font-label-md text-label-md text-primary/70 uppercase tracking-wider text-[10px]">Terminal Active</div>
</div>
</div>
<!-- Main Tabs -->
<nav class="flex-1 overflow-y-auto">
<ul class="space-y-2">
<li>
<a class="flex items-center px-4 py-3 bg-primary-container text-on-primary-container rounded-lg mx-2 group/item transition-all duration-300" href="#">
<span class="material-symbols-outlined shrink-0" data-icon="dashboard">dashboard</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Dashboard</span>
</a>
</li>
<li>
<a class="flex items-center px-4 py-3 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg group/item transition-all duration-300" href="#">
<span class="material-symbols-outlined shrink-0" data-icon="security_update_warning">security_update_warning</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Risk Analysis</span>
</a>
</li>
<li>
<a class="flex items-center px-4 py-3 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg group/item transition-all duration-300" href="#">
<span class="material-symbols-outlined shrink-0" data-icon="monitoring">monitoring</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Telemetry</span>
</a>
</li>
<li>
<a class="flex items-center px-4 py-3 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg group/item transition-all duration-300" href="#">
<span class="material-symbols-outlined shrink-0" data-icon="fact_check">fact_check</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Audits</span>
</a>
</li>
<li>
<a class="flex items-center px-4 py-3 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg group/item transition-all duration-300" href="#">
<span class="material-symbols-outlined shrink-0" data-icon="settings">settings</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Settings</span>
</a>
</li>
</ul>
</nav>
<!-- CTA -->
<div class="px-4 my-6 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">
<button class="w-full bg-primary/10 hover:bg-primary/20 border border-primary text-primary font-label-md text-label-md uppercase tracking-wider py-2 rounded-lg transition-colors flex items-center justify-center gap-2">
<span class="material-symbols-outlined text-[18px]" data-icon="download">download</span>
                    Export Report
                </button>
</div>
<!-- Footer Tabs -->
<div class="mt-auto border-t border-white/5 pt-4">
<ul class="space-y-2">
<li>
<a class="flex items-center px-4 py-2 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg group/item transition-all duration-300" href="#">
<span class="material-symbols-outlined shrink-0" data-icon="help">help</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Support</span>
</a>
</li>
<li>
<a class="flex items-center px-4 py-2 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg group/item transition-all duration-300" href="#">
<span class="material-symbols-outlined shrink-0" data-icon="logout">logout</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Logout</span>
</a>
</li>
</ul>
</div>
</aside>
<!-- Main Canvas -->
<main class="flex-1 md:ml-20 w-full overflow-y-auto bg-background px-4 md:px-container-padding py-8 md:pt-24 pb-24 relative z-10">
<!-- Global Environment Banner -->
<div class="mb-6 flex items-center justify-center w-full py-1.5 glass-panel rounded-md border-tertiary/30 bg-tertiary/5 text-tertiary font-mono-data text-mono-data">
<span class="material-symbols-outlined text-[16px] mr-2" data-icon="science">science</span>
                Entorno de demostración · Datos sintéticos
            </div>
<!-- Page Header -->
<header class="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
<div>
<h1 class="font-headline-lg text-headline-lg text-on-surface tracking-tight mb-1">Auditor Terminal</h1>
<p class="font-body-md text-body-md text-on-surface-variant">Real-time oversight and anomaly detection for primary nodes.</p>
</div>
<div class="flex items-center gap-3">
<span class="flex items-center gap-2 font-mono-data text-mono-data text-primary-fixed bg-primary-fixed/10 px-3 py-1.5 rounded border border-primary-fixed/20">
<span class="w-2 h-2 rounded-full bg-primary-fixed animate-pulse"></span>
                        SYSTEM ONLINE
                    </span>
<span class="font-mono-data text-mono-data text-on-surface-variant px-3 py-1.5 rounded glass-panel">
                        UTC-5 14:32:01
                    </span>
</div>
</header>
<!-- KPI Bento Grid -->
<section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
<!-- KPI 1: Active Alerts -->
<div class="glass-card rounded-xl p-5 relative overflow-hidden group">
<div class="absolute inset-0 bg-gradient-to-br from-error/5 to-transparent opacity-50"></div>
<div class="relative z-10 flex flex-col h-full justify-between gap-4">
<div class="flex justify-between items-start">
<span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Active Alerts</span>
<div class="w-8 h-8 rounded-full bg-error/10 flex items-center justify-center border border-error/20 pulse-border">
<span class="material-symbols-outlined text-error text-[18px]" data-icon="warning">warning</span>
</div>
</div>
<div>
<div class="flex items-baseline gap-3">
<span class="font-display-lg text-display-lg text-error">14</span>
<span class="flex items-center font-mono-data text-mono-data text-error bg-error/10 px-1.5 py-0.5 rounded">
<span class="material-symbols-outlined text-[14px]" data-icon="arrow_upward">arrow_upward</span>
                                    5%
                                </span>
</div>
</div>
</div>
<!-- Abstract sparkline representation -->
<div class="absolute bottom-0 left-0 w-full h-12 opacity-30 pointer-events-none">
<svg class="w-full h-full stroke-error fill-none" preserveaspectratio="none" stroke-width="2" viewbox="0 0 100 30">
<path d="M0,25 L10,22 L20,28 L30,15 L40,18 L50,10 L60,12 L70,5 L80,8 L90,2 L100,0"></path>
</svg>
<svg class="w-full h-full fill-error/20 absolute bottom-0 left-0" preserveaspectratio="none" viewbox="0 0 100 30">
<path d="M0,30 L0,25 L10,22 L20,28 L30,15 L40,18 L50,10 L60,12 L70,5 L80,8 L90,2 L100,0 L100,30 Z"></path>
</svg>
</div>
</div>
<!-- KPI 2: Operations Analyzed -->
<div class="glass-card rounded-xl p-5 relative overflow-hidden">
<div class="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent opacity-50"></div>
<div class="relative z-10 flex flex-col h-full justify-between gap-4">
<div class="flex justify-between items-start">
<span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Operations Analyzed</span>
<div class="w-8 h-8 rounded-full bg-surface-container-high flex items-center justify-center border border-white/10">
<span class="material-symbols-outlined text-on-surface-variant text-[18px]" data-icon="dataset">dataset</span>
</div>
</div>
<div>
<div class="flex items-baseline gap-3">
<span class="font-display-lg text-display-lg text-on-surface">1,240</span>
<span class="font-body-sm text-body-sm text-on-surface-variant">daily vol.</span>
</div>
</div>
</div>
</div>
<!-- KPI 3: Model F1-Score -->
<div class="glass-card rounded-xl p-5 relative overflow-hidden">
<div class="absolute inset-0 bg-gradient-to-br from-tertiary/5 to-transparent opacity-50"></div>
<div class="relative z-10 flex flex-col h-full justify-between gap-4">
<div class="flex justify-between items-start">
<span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Model F1-Score</span>
<div class="w-8 h-8 rounded-full bg-tertiary/10 flex items-center justify-center border border-tertiary/20">
<span class="material-symbols-outlined text-tertiary text-[18px]" data-icon="model_training">model_training</span>
</div>
</div>
<div>
<div class="flex items-baseline gap-3">
<span class="font-display-lg text-display-lg text-tertiary">0.92</span>
<span class="font-body-sm text-body-sm text-tertiary/80 bg-tertiary/10 px-2 py-0.5 rounded border border-tertiary/20">high conf</span>
</div>
</div>
</div>
</div>
<!-- KPI 4: Avg Decision Time -->
<div class="glass-card rounded-xl p-5 relative overflow-hidden">
<div class="absolute inset-0 bg-gradient-to-br from-secondary/5 to-transparent opacity-50"></div>
<div class="relative z-10 flex flex-col h-full justify-between gap-4">
<div class="flex justify-between items-start">
<span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Avg. Decision Time</span>
<div class="w-8 h-8 rounded-full bg-secondary/10 flex items-center justify-center border border-secondary/20">
<span class="material-symbols-outlined text-secondary text-[18px]" data-icon="timer">timer</span>
</div>
</div>
<div>
<div class="flex items-baseline gap-3">
<span class="font-display-lg text-display-lg text-on-surface">42s</span>
<span class="flex items-center font-mono-data text-mono-data text-secondary bg-secondary/10 px-1.5 py-0.5 rounded">
<span class="material-symbols-outlined text-[14px]" data-icon="arrow_downward">arrow_downward</span>
                                    2s
                                </span>
</div>
</div>
</div>
</div>
</section>
<!-- Main Layout Grid -->
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
<!-- Center Column (Chart & Table) -->
<div class="lg:col-span-2 flex flex-col gap-6">
<!-- Alert Trends Chart Container -->
<div class="glass-card rounded-xl p-6 h-80 flex flex-col">
<div class="flex justify-between items-center mb-6">
<h2 class="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2">
<span class="material-symbols-outlined text-primary" data-icon="show_chart">show_chart</span>
                                Alert Trends (14 Days)
                            </h2>
<div class="flex gap-2">
<button class="px-3 py-1 font-label-md text-label-md text-on-surface-variant bg-surface-container-high rounded border border-white/5 hover:text-primary transition-colors">7D</button>
<button class="px-3 py-1 font-label-md text-label-md text-on-primary-container bg-primary-container rounded border border-primary/30">14D</button>
<button class="px-3 py-1 font-label-md text-label-md text-on-surface-variant bg-surface-container-high rounded border border-white/5 hover:text-primary transition-colors">30D</button>
</div>
</div>
<!-- Simulated Chart Area using Grid & CSS -->
<div class="flex-1 relative w-full border-b border-l border-white/10 flex items-end pt-4 pb-2 pr-2">
<!-- Y-axis labels -->
<div class="absolute left-[-24px] top-0 bottom-0 flex flex-col justify-between text-[10px] font-mono-data text-on-surface-variant py-2">
<span>20</span>
<span>15</span>
<span>10</span>
<span>5</span>
<span>0</span>
</div>
<!-- Grid lines -->
<div class="absolute inset-0 flex flex-col justify-between pointer-events-none z-0 px-2 py-2">
<div class="w-full border-t border-white/5 h-0"></div>
<div class="w-full border-t border-white/5 h-0"></div>
<div class="w-full border-t border-white/5 h-0"></div>
<div class="w-full border-t border-white/5 h-0"></div>
<div class="w-full border-t border-white/5 h-0"></div>
</div>
<!-- Simulated Line Chart -->
<div class="relative w-full h-full z-10 flex items-end">
<svg class="absolute inset-0 w-full h-full stroke-primary fill-none overflow-visible" preserveaspectratio="none" stroke-width="2" vector-effect="non-scaling-stroke" viewbox="0 0 100 100">
<path d="M0,80 L8,75 L16,60 L24,65 L32,40 L40,45 L48,30 L56,50 L64,20 L72,35 L80,10 L88,25 L96,5 L100,5" stroke-linejoin="round"></path>
</svg>
<!-- Area fill -->
<svg class="absolute inset-0 w-full h-full fill-primary/10" overflow="visible" preserveaspectratio="none" viewbox="0 0 100 100">
<path d="M0,100 L0,80 L8,75 L16,60 L24,65 L32,40 L40,45 L48,30 L56,50 L64,20 L72,35 L80,10 L88,25 L96,5 L100,5 L100,100 Z"></path>
</svg>
<!-- Data points (hover targets) -->
<div class="absolute w-full h-full flex justify-between items-end px-[0.5%]">
<div class="w-2 h-2 rounded-full bg-primary border border-background absolute" style="left: 0%; bottom: 20%;"></div>
<div class="w-2 h-2 rounded-full bg-primary border border-background absolute" style="left: 32%; bottom: 60%;"></div>
<div class="w-2 h-2 rounded-full bg-error border border-background absolute animate-pulse" style="left: 80%; bottom: 90%;"></div>
<div class="w-2 h-2 rounded-full bg-primary border border-background absolute" style="left: 100%; bottom: 95%;"></div>
</div>
</div>
<!-- X-axis labels -->
<div class="absolute bottom-[-20px] left-0 right-0 flex justify-between text-[10px] font-mono-data text-on-surface-variant px-2">
<span>D-14</span>
<span>D-10</span>
<span>D-5</span>
<span>Today</span>
</div>
</div>
</div>
<!-- Priority Alerts Table -->
<div class="glass-card rounded-xl flex flex-col overflow-hidden">
<div class="p-6 border-b border-white/5 flex justify-between items-center bg-surface-container/20">
<h2 class="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2">
<span class="material-symbols-outlined text-error" data-icon="policy">policy</span>
                                Priority Alerts Queue
                            </h2>
<button class="text-primary hover:text-primary-fixed text-sm font-label-md flex items-center gap-1 transition-colors">
                                View All
                                <span class="material-symbols-outlined text-[16px]" data-icon="arrow_forward">arrow_forward</span>
</button>
</div>
<div class="overflow-x-auto w-full">
<table class="w-full text-left border-collapse min-w-[600px]">
<thead>
<tr class="bg-surface-container-high/50 border-b-2 border-primary/30">
<th class="py-3 px-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Alert ID</th>
<th class="py-3 px-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Product</th>
<th class="py-3 px-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Exportadora</th>
<th class="py-3 px-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Severity</th>
<th class="py-3 px-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider text-right">Action</th>
</tr>
</thead>
<tbody class="font-mono-data text-mono-data">
<!-- Row 1 (High Severity) -->
<tr class="border-b border-white/5 hover:bg-white/[0.02] transition-colors group">
<td class="py-3 px-4 text-on-surface">AL-2026-0012</td>
<td class="py-3 px-4">
<span class="inline-flex items-center px-2 py-1 rounded bg-surface-variant text-on-surface-variant border border-white/10 font-body-sm text-body-sm">
<span class="w-2 h-2 rounded-full bg-[#4A7C59] mr-2"></span>Palta
                                            </span>
</td>
<td class="py-3 px-4 text-on-surface-variant">AgroExport Sur S.A.</td>
<td class="py-3 px-4">
<div class="flex items-center gap-2">
<div class="w-16 h-1.5 bg-surface-container-highest rounded-full overflow-hidden">
<div class="h-full bg-error w-[95%]"></div>
</div>
<span class="text-error font-bold">0.95</span>
</div>
</td>
<td class="py-3 px-4 text-right">
<button class="px-3 py-1 bg-transparent border border-error text-error rounded hover:bg-error/10 transition-colors font-label-md text-label-md uppercase opacity-80 group-hover:opacity-100">Audit</button>
</td>
</tr>
<!-- Row 2 (Medium Severity) -->
<tr class="border-b border-white/5 hover:bg-white/[0.02] transition-colors group">
<td class="py-3 px-4 text-on-surface">AL-2026-0011</td>
<td class="py-3 px-4">
<span class="inline-flex items-center px-2 py-1 rounded bg-surface-variant text-on-surface-variant border border-white/10 font-body-sm text-body-sm">
<span class="w-2 h-2 rounded-full bg-[#8B5A8C] mr-2"></span>Uva
                                            </span>
</td>
<td class="py-3 px-4 text-on-surface-variant">Valles del Norte EIRL</td>
<td class="py-3 px-4">
<div class="flex items-center gap-2">
<div class="w-16 h-1.5 bg-surface-container-highest rounded-full overflow-hidden">
<div class="h-full bg-secondary w-[72%]"></div>
</div>
<span class="text-secondary font-bold">0.72</span>
</div>
</td>
<td class="py-3 px-4 text-right">
<button class="px-3 py-1 bg-transparent border border-primary text-primary rounded hover:bg-primary/10 transition-colors font-label-md text-label-md uppercase opacity-80 group-hover:opacity-100">Review</button>
</td>
</tr>
<!-- Row 3 (Medium-Low Severity) -->
<tr class="hover:bg-white/[0.02] transition-colors group">
<td class="py-3 px-4 text-on-surface">AL-2026-0010</td>
<td class="py-3 px-4">
<span class="inline-flex items-center px-2 py-1 rounded bg-surface-variant text-on-surface-variant border border-white/10 font-body-sm text-body-sm">
<span class="w-2 h-2 rounded-full bg-[#3B5998] mr-2"></span>Arándano
                                            </span>
</td>
<td class="py-3 px-4 text-on-surface-variant">BerryCorp Andina</td>
<td class="py-3 px-4">
<div class="flex items-center gap-2">
<div class="w-16 h-1.5 bg-surface-container-highest rounded-full overflow-hidden">
<div class="h-full bg-primary-fixed-dim w-[65%]"></div>
</div>
<span class="text-primary-fixed-dim font-bold">0.65</span>
</div>
</td>
<td class="py-3 px-4 text-right">
<button class="px-3 py-1 bg-transparent border border-primary text-primary rounded hover:bg-primary/10 transition-colors font-label-md text-label-md uppercase opacity-80 group-hover:opacity-100">Review</button>
</td>
</tr>
</tbody>
</table>
</div>
</div>
</div>
<!-- Right Column (Activity Feed) -->
<div class="glass-card rounded-xl flex flex-col h-[calc(100vh-16rem)] min-h-[500px]">
<div class="p-6 border-b border-white/5 bg-surface-container/20 shrink-0">
<h2 class="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2">
<span class="material-symbols-outlined text-tertiary" data-icon="history">history</span>
                            System Telemetry Feed
                        </h2>
</div>
<div class="p-6 overflow-y-auto flex-1 relative">
<!-- Timeline track -->
<div class="absolute left-8 top-6 bottom-6 w-px bg-white/10 z-0"></div>
<ul class="space-y-6 relative z-10">
<!-- Feed Item 1 -->
<li class="flex gap-4">
<div class="w-4 h-4 rounded-full bg-error border-[3px] border-background shrink-0 mt-1 relative z-10 animate-pulse shadow-[0_0_8px_rgba(255,180,171,0.6)]"></div>
<div>
<div class="font-mono-data text-mono-data text-on-surface-variant text-[10px] mb-1">Jus now · Node Alpha</div>
<div class="font-body-sm text-body-sm text-on-surface font-medium">Alerta de anomalía crítica</div>
<div class="font-body-sm text-body-sm text-error mt-1 glass-panel p-2 rounded border-error/20 inline-block">Score de varianza: &gt;3σ en humedad de envío</div>
</div>
</li>
<!-- Feed Item 2 -->
<li class="flex gap-4">
<div class="w-4 h-4 rounded-full bg-tertiary border-[3px] border-background shrink-0 mt-1 relative z-10"></div>
<div>
<div class="font-mono-data text-mono-data text-on-surface-variant text-[10px] mb-1">-12 min · Auto-System</div>
<div class="font-body-sm text-body-sm text-on-surface font-medium">Dataset updated</div>
<div class="font-body-sm text-body-sm text-on-surface-variant mt-1">Sincronización de lote LT-998 completada (1.2k registros).</div>
</div>
</li>
<!-- Feed Item 3 -->
<li class="flex gap-4">
<div class="w-4 h-4 rounded-full bg-primary border-[3px] border-background shrink-0 mt-1 relative z-10"></div>
<div>
<div class="font-mono-data text-mono-data text-on-surface-variant text-[10px] mb-1">-45 min · Auditor ID: A-442</div>
<div class="font-body-sm text-body-sm text-on-surface font-medium">Alerta confirmada por Auditor A</div>
<div class="font-body-sm text-body-sm text-on-surface-variant mt-1 flex items-center gap-2">
<span class="material-symbols-outlined text-[14px] text-primary" data-icon="check_circle">check_circle</span>
                                        Resolución aplicada a AL-2026-0009.
                                    </div>
</div>
</li>
<!-- Feed Item 4 -->
<li class="flex gap-4">
<div class="w-4 h-4 rounded-full bg-surface-variant border-[3px] border-background shrink-0 mt-1 relative z-10"></div>
<div>
<div class="font-mono-data text-mono-data text-on-surface-variant text-[10px] mb-1">-2 hrs · System Routine</div>
<div class="font-body-sm text-body-sm text-on-surface-variant font-medium">Calibración de modelo predictivo</div>
<div class="font-body-sm text-body-sm text-on-surface-variant/70 mt-1">Ajuste de pesos base. F1-Score estable.</div>
</div>
</li>
<!-- Feed Item 5 -->
<li class="flex gap-4 opacity-50">
<div class="w-4 h-4 rounded-full bg-surface-variant border-[3px] border-background shrink-0 mt-1 relative z-10"></div>
<div>
<div class="font-mono-data text-mono-data text-on-surface-variant text-[10px] mb-1">-5 hrs · Admin</div>
<div class="font-body-sm text-body-sm text-on-surface-variant font-medium">Sesión iniciada</div>
</div>
</li>
</ul>
</div>
<div class="p-4 border-t border-white/5 bg-surface-container/10 mt-auto">
<button class="w-full text-center text-primary font-label-md text-label-md hover:text-primary-fixed transition-colors">Load Archive Logs</button>
</div>
</div>
</div>
</main>
</div>
<!-- Mobile Bottom Nav (Visible only on md hidden) -->
<nav class="md:hidden fixed bottom-0 w-full h-16 bg-surface-container/80 backdrop-blur-xl border-t border-white/5 z-50 flex justify-around items-center px-2 pb-safe">
<a class="flex flex-col items-center justify-center w-16 h-full text-primary" href="#">
<div class="w-12 h-8 bg-primary-container rounded-full flex items-center justify-center mb-1">
<span class="material-symbols-outlined text-on-primary-container" data-icon="dashboard">dashboard</span>
</div>
<span class="font-label-md text-[10px] tracking-tight">Inicio</span>
</a>
<a class="flex flex-col items-center justify-center w-16 h-full text-on-surface-variant hover:text-primary transition-colors" href="#">
<div class="w-12 h-8 flex items-center justify-center mb-1">
<span class="material-symbols-outlined" data-icon="fact_check">fact_check</span>
</div>
<span class="font-label-md text-[10px] tracking-tight">Alertas</span>
</a>
<a class="flex flex-col items-center justify-center w-16 h-full text-on-surface-variant hover:text-primary transition-colors" href="#">
<div class="w-12 h-8 flex items-center justify-center mb-1">
<span class="material-symbols-outlined" data-icon="monitoring">monitoring</span>
</div>
<span class="font-label-md text-[10px] tracking-tight">Métricas</span>
</a>
<a class="flex flex-col items-center justify-center w-16 h-full text-on-surface-variant hover:text-primary transition-colors" href="#">
<div class="w-12 h-8 flex items-center justify-center mb-1">
<span class="material-symbols-outlined" data-icon="person">person</span>
</div>
<span class="font-label-md text-[10px] tracking-tight">Perfil</span>
</a>
</nav>
</body></html>

<!-- My Audit History -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Audit History - Agro-Intelligence Oversight</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Outfit:wght@600;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    "colors": {
                        "outline-variant": "#3f4a3f",
                        "surface-container-low": "#171d17",
                        "primary-container": "#3da35d",
                        "surface-container-lowest": "#0a100a",
                        "on-secondary-fixed-variant": "#1e502e",
                        "inverse-on-surface": "#2c322b",
                        "surface-container": "#1b211b",
                        "surface-variant": "#30362f",
                        "surface-container-highest": "#30362f",
                        "inverse-primary": "#006d33",
                        "primary-fixed": "#92f8a9",
                        "on-surface-variant": "#becabc",
                        "tertiary-fixed-dim": "#89ceff",
                        "on-surface": "#dee4da",
                        "surface-tint": "#76db8f",
                        "tertiary-fixed": "#c9e6ff",
                        "on-error-container": "#ffdad6",
                        "on-tertiary-fixed": "#001e2f",
                        "on-background": "#dee4da",
                        "on-tertiary-fixed-variant": "#004c6e",
                        "error-container": "#93000a",
                        "secondary-container": "#205331",
                        "primary-fixed-dim": "#76db8f",
                        "on-secondary-container": "#8fc599",
                        "on-primary-container": "#003114",
                        "tertiary": "#89ceff",
                        "surface-bright": "#343b34",
                        "secondary": "#9dd3a7",
                        "on-primary-fixed": "#00210b",
                        "on-tertiary": "#00344d",
                        "on-primary": "#003918",
                        "secondary-fixed": "#b8f0c2",
                        "background": "#0f150f",
                        "outline": "#889487",
                        "tertiary-container": "#009ada",
                        "primary": "#76db8f",
                        "on-tertiary-container": "#002d43",
                        "surface-container-high": "#252c25",
                        "surface-dim": "#0f150f",
                        "on-error": "#690005",
                        "inverse-surface": "#dee4da",
                        "surface": "#0f150f",
                        "on-secondary-fixed": "#00210c",
                        "on-primary-fixed-variant": "#005225",
                        "on-secondary": "#01391a",
                        "secondary-fixed-dim": "#9dd3a7",
                        "error": "#ffb4ab"
                    },
                    "borderRadius": {
                        "DEFAULT": "0.125rem",
                        "lg": "0.25rem",
                        "xl": "0.5rem",
                        "full": "0.75rem"
                    },
                    "spacing": {
                        "gutter": "16px",
                        "card-gap": "20px",
                        "container-padding": "24px",
                        "unit": "4px"
                    },
                    "fontFamily": {
                        "body-md": ["Inter"],
                        "headline-sm": ["Outfit"],
                        "body-sm": ["Inter"],
                        "headline-md": ["Outfit"],
                        "display-lg": ["Outfit"],
                        "headline-lg": ["Outfit"],
                        "mono-data": ["monospace"],
                        "label-md": ["Inter"],
                        "body-lg": ["Inter"]
                    },
                    "fontSize": {
                        "body-md": ["16px", { "lineHeight": "24px", "fontWeight": "400" }],
                        "headline-sm": ["20px", { "lineHeight": "28px", "fontWeight": "600" }],
                        "body-sm": ["14px", { "lineHeight": "20px", "fontWeight": "400" }],
                        "headline-md": ["24px", { "lineHeight": "32px", "fontWeight": "600" }],
                        "display-lg": ["48px", { "lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "700" }],
                        "headline-lg": ["32px", { "lineHeight": "40px", "fontWeight": "600" }],
                        "mono-data": ["14px", { "lineHeight": "20px", "fontWeight": "500" }],
                        "label-md": ["12px", { "lineHeight": "16px", "letterSpacing": "0.05em", "fontWeight": "600" }],
                        "body-lg": ["18px", { "lineHeight": "28px", "fontWeight": "400" }]
                    }
                }
            }
        }
    </script>
<style>
        .glass-panel {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .glass-input {
            background: transparent;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }
        .glass-input:focus {
            background: rgba(255, 255, 255, 0.06);
            border-color: #3da35d;
            box-shadow: 0 0 0 1px #3da35d;
        }
        .audit-table tr:nth-child(even) {
            background: rgba(255, 255, 255, 0.02);
        }
        .table-header {
            background: rgba(255, 255, 255, 0.05);
            border-bottom: 2px solid #76db8f;
        }
        .pulse-border {
            animation: pulse-border 2s infinite;
        }
        @keyframes pulse-border {
            0% { box-shadow: 0 0 0 0 rgba(255, 180, 171, 0.4); }
            70% { box-shadow: 0 0 0 6px rgba(255, 180, 171, 0); }
            100% { box-shadow: 0 0 0 0 rgba(255, 180, 171, 0); }
        }
    </style>
</head>
<body class="bg-background text-on-surface antialiased min-h-screen flex flex-col md:flex-row overflow-hidden">
<!-- Mobile Top App Bar -->
<header class="md:hidden bg-surface-container/40 dark:bg-surface-container/40 backdrop-blur-xl shadow-sm border-b border-white/10 flex justify-between items-center px-container-padding w-full h-16 shrink-0 z-40">
<div class="font-headline-md text-headline-md font-bold text-primary">Agro-Intelligence Oversight</div>
<div class="flex items-center gap-4">
<span class="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors cursor-pointer active:scale-95">notifications</span>
<span class="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors cursor-pointer active:scale-95">settings</span>
<img alt="Auditor Profile" class="w-8 h-8 rounded-full border border-primary/30 object-cover" data-alt="A small, circular avatar portrait of an auditor in a high-tech control room environment, bathed in subtle green light, dark theme, sharp focus." src="https://lh3.googleusercontent.com/aida-public/AB6AXuAMT25hUIeeOCu4-Pj90xf777MdtK_EXYMxhFJxhAg_hbKCqYNe13-PPBuA4F2ZIs0Njl28fduXnLr4r2RTjuy2UV56Cmcmembb5x7-9EJiYoORC1FEPr7AIY8nGBKK1RTD5tl3DDqYtflQVdj8iVcMBvo9kUVohL9wLZLFOY5rC2Ygo4M4DihjrhutIgVtt0lHNnzEcNul-TE9k9ueIh1hWKAqLbNb-hr3BGA7mUy8eJBhd-D9UfKGh6XeCp6e-Rq6S-yUtcapdNE"/>
</div>
</header>
<!-- Sidebar Navigation (Desktop) -->
<nav class="hidden md:flex flex-col py-6 h-full bg-surface-container-lowest dark:bg-surface-container-lowest border-r border-white/5 shadow-2xl h-screen w-20 hover:w-64 transition-all duration-300 ease-in-out fixed left-0 top-0 z-50 group shrink-0">
<div class="px-4 flex items-center gap-4 mb-8 overflow-hidden whitespace-nowrap">
<img alt="System Logo" class="w-10 h-10 rounded-lg shrink-0" data-alt="A stylized, glowing geometric hexagon logo representing a high-tech terminal, dark theme, sharp and pristine, emerald green accents." src="https://lh3.googleusercontent.com/aida-public/AB6AXuBd7Zr28GvYrLwtbFUgrHSoZZkCL5QP2TjcVTm24T1S2AHNjjhTugu0ukKiHN47xvRMM7nazLi2wXbKPhV3fwrrfWxH3loraDGd00roF0FxVz1s9Ur7-TXME_zs9jkioDDlShknRxSXibYdBFobjntg9KOFOsc2JEynkl0cZCpd2amz32bb6Gttdabxb0cqzg3D3PCKawvy7C8MTnmeDcQkhIPTyosXCJpYAY3BufR-DYAZMqH3g7EvrI2CeahBXn7SkkWpVOQlrB0"/>
<div class="opacity-0 group-hover:opacity-100 transition-opacity duration-300">
<div class="font-headline-sm text-headline-sm text-primary-fixed">AUDIT_OS_V1</div>
<div class="font-label-md text-label-md uppercase tracking-wider text-primary">Terminal Active</div>
</div>
</div>
<div class="flex flex-col gap-2 flex-grow overflow-hidden whitespace-nowrap">
<a class="flex items-center gap-4 py-3 px-4 text-on-surface-variant hover:text-primary mx-2 rounded-lg hover:bg-surface-variant/20 transition-colors" href="#">
<span class="material-symbols-outlined shrink-0">dashboard</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300">Dashboard</span>
</a>
<a class="flex items-center gap-4 py-3 px-4 text-on-surface-variant hover:text-primary mx-2 rounded-lg hover:bg-surface-variant/20 transition-colors" href="#">
<span class="material-symbols-outlined shrink-0">security_update_warning</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300">Risk Analysis</span>
</a>
<a class="flex items-center gap-4 py-3 px-4 text-on-surface-variant hover:text-primary mx-2 rounded-lg hover:bg-surface-variant/20 transition-colors" href="#">
<span class="material-symbols-outlined shrink-0">monitoring</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300">Telemetry</span>
</a>
<a class="flex items-center gap-4 py-3 px-4 bg-primary-container text-on-primary-container rounded-lg mx-2 transition-colors" href="#">
<span class="material-symbols-outlined shrink-0" style="font-variation-settings: 'FILL' 1;">fact_check</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300">Audits</span>
</a>
<a class="flex items-center gap-4 py-3 px-4 text-on-surface-variant hover:text-primary mx-2 rounded-lg hover:bg-surface-variant/20 transition-colors" href="#">
<span class="material-symbols-outlined shrink-0">settings</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300">Settings</span>
</a>
</div>
<div class="px-4 mt-auto mb-4 overflow-hidden whitespace-nowrap">
<button class="w-full py-2 bg-primary/10 text-primary border border-primary/30 rounded-lg font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 hover:bg-primary/20">
                Export Report
            </button>
</div>
<div class="flex flex-col gap-2 overflow-hidden whitespace-nowrap border-t border-white/5 pt-4">
<a class="flex items-center gap-4 py-3 px-4 text-on-surface-variant hover:text-primary mx-2 rounded-lg hover:bg-surface-variant/20 transition-colors" href="#">
<span class="material-symbols-outlined shrink-0">help</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300">Support</span>
</a>
<a class="flex items-center gap-4 py-3 px-4 text-on-surface-variant hover:text-primary mx-2 rounded-lg hover:bg-surface-variant/20 transition-colors" href="#">
<span class="material-symbols-outlined shrink-0">logout</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300">Logout</span>
</a>
</div>
</nav>
<!-- Main Content Canvas -->
<main class="flex-grow md:ml-20 flex flex-col h-screen overflow-hidden bg-background relative z-0">
<!-- Optional Top Nav TopAppBar (Web) to match context if needed, but since Sidebar is the main nav, we'll focus on content -->
<div class="hidden md:flex justify-between items-center px-container-padding py-4 border-b border-white/5 glass-panel z-10 shrink-0 sticky top-0">
<div class="font-headline-md text-headline-md font-bold text-primary">Audits</div>
<div class="flex items-center gap-6">
<div class="relative">
<span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-sm">search</span>
<input class="glass-input pl-10 pr-4 py-2 rounded-lg font-body-sm text-body-sm text-on-surface placeholder-on-surface-variant w-64 focus:outline-none" placeholder="Search Audit ID..." type="text"/>
</div>
<div class="flex items-center gap-4">
<span class="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors cursor-pointer">notifications</span>
<img alt="Auditor Profile" class="w-8 h-8 rounded-full border border-primary/30 object-cover" data-alt="A small, circular avatar portrait of an auditor in a high-tech control room environment, bathed in subtle green light, dark theme, sharp focus." src="https://lh3.googleusercontent.com/aida-public/AB6AXuBtU-b-sU7UbuS78vQm29szMDfOPz1asv9ngZpBbRdfcylhnVexiSqGuLkCzWf-tLgoSDXAqM4dX0xdmRVSfqiljvwOLmEyjPROAtPQl10wrOCQ0Z_7gvZ14NCHqllGd3XkSE6q-qhDtwgYKLETle8bSvYtV74R9ZqV-WGy29mYB_AMSauQJ9JNwvbXZ088jUBYbTb4gXt-o8naIPNloZy4pmIBgF6_l7RTpsQEwqCL0Lr7IH2iGJcEqZRbbEwXwxYWZxh4VkgY6f0"/>
</div>
</div>
</div>
<div class="p-container-padding flex-grow overflow-y-auto overflow-x-hidden">
<!-- Header & Controls -->
<div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-card-gap">
<div>
<h1 class="font-headline-lg text-headline-lg text-on-surface">Audit History</h1>
<p class="font-body-sm text-body-sm text-on-surface-variant mt-1">Review your previous operational classifications.</p>
</div>
<div class="flex flex-wrap items-center gap-4 glass-panel p-2 rounded-lg">
<div class="flex items-center gap-2 px-2">
<span class="material-symbols-outlined text-primary text-sm">filter_list</span>
<span class="font-label-md text-label-md text-on-surface-variant">Condition Filter:</span>
</div>
<div class="flex gap-1 bg-surface-container-highest p-1 rounded-md">
<button class="px-4 py-1.5 rounded bg-primary-container text-on-primary-container font-label-md text-label-md transition-colors">All</button>
<button class="px-4 py-1.5 rounded text-on-surface-variant hover:bg-surface-variant/50 font-label-md text-label-md transition-colors">Integrated</button>
<button class="px-4 py-1.5 rounded text-on-surface-variant hover:bg-surface-variant/50 font-label-md text-label-md transition-colors">Aislado</button>
</div>
</div>
</div>
<!-- Main Data Table Container -->
<div class="glass-panel rounded-xl overflow-hidden flex flex-col relative min-h-[500px]">
<div class="overflow-x-auto">
<table class="w-full text-left border-collapse audit-table whitespace-nowrap">
<thead class="table-header">
<tr>
<th class="py-4 px-4 font-label-md text-label-md text-primary uppercase tracking-wider">Decision ID</th>
<th class="py-4 px-4 font-label-md text-label-md text-primary uppercase tracking-wider">Alert ID</th>
<th class="py-4 px-4 font-label-md text-label-md text-primary uppercase tracking-wider">Product</th>
<th class="py-4 px-4 font-label-md text-label-md text-primary uppercase tracking-wider">Final Classification</th>
<th class="py-4 px-4 font-label-md text-label-md text-primary uppercase tracking-wider text-center">Score</th>
<th class="py-4 px-4 font-label-md text-label-md text-primary uppercase tracking-wider text-right">Time (ms)</th>
<th class="py-4 px-4 font-label-md text-label-md text-primary uppercase tracking-wider">Date</th>
<th class="py-4 px-4 font-label-md text-label-md text-primary uppercase tracking-wider text-right">Action</th>
</tr>
</thead>
<tbody class="font-mono-data text-mono-data text-on-surface divide-y divide-white/5">
<!-- Row 1 -->
<tr class="hover:bg-white/5 transition-colors group">
<td class="py-3 px-4">DEC-9821</td>
<td class="py-3 px-4 text-on-surface-variant">ALT-001A</td>
<td class="py-3 px-4">
<div class="flex items-center gap-2">
<span class="w-2 h-2 rounded-full bg-tertiary"></span>
                                        Avocado Hass
                                    </div>
</td>
<td class="py-3 px-4">
<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-error-container/20 text-error border border-error/30 pulse-border">
<span class="material-symbols-outlined text-[14px]">warning</span>
                                        Confirmed
                                    </span>
</td>
<td class="py-3 px-4 text-center">
<div class="flex justify-center items-center gap-1 text-primary">
<span class="material-symbols-outlined text-[14px]" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-[14px]" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-[14px]" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-[14px]" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-[14px]">star</span>
</div>
</td>
<td class="py-3 px-4 text-right">4,201</td>
<td class="py-3 px-4 text-on-surface-variant">2023-10-27 14:32:01</td>
<td class="py-3 px-4 text-right">
<button class="opacity-0 group-hover:opacity-100 transition-opacity bg-primary/10 hover:bg-primary/20 text-primary border border-primary/30 px-3 py-1.5 rounded font-label-md text-label-md">
                                        Review Detail
                                    </button>
</td>
</tr>
<!-- Row 2 -->
<tr class="hover:bg-white/5 transition-colors group">
<td class="py-3 px-4">DEC-9820</td>
<td class="py-3 px-4 text-on-surface-variant">ALT-002B</td>
<td class="py-3 px-4">
<div class="flex items-center gap-2">
<span class="w-2 h-2 rounded-full bg-secondary"></span>
                                        Mango Kent
                                    </div>
</td>
<td class="py-3 px-4">
<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-surface-variant text-on-surface-variant border border-white/10">
<span class="material-symbols-outlined text-[14px]">check_circle</span>
                                        Falsa Alarma
                                    </span>
</td>
<td class="py-3 px-4 text-center">
<div class="flex justify-center items-center gap-1 text-primary">
<span class="material-symbols-outlined text-[14px]" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-[14px]" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-[14px]" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-[14px]">star</span>
<span class="material-symbols-outlined text-[14px]">star</span>
</div>
</td>
<td class="py-3 px-4 text-right">8,450</td>
<td class="py-3 px-4 text-on-surface-variant">2023-10-27 14:15:22</td>
<td class="py-3 px-4 text-right">
<button class="opacity-0 group-hover:opacity-100 transition-opacity bg-primary/10 hover:bg-primary/20 text-primary border border-primary/30 px-3 py-1.5 rounded font-label-md text-label-md">
                                        Review Detail
                                    </button>
</td>
</tr>
<!-- Row 3 -->
<tr class="hover:bg-white/5 transition-colors group">
<td class="py-3 px-4">DEC-9819</td>
<td class="py-3 px-4 text-on-surface-variant">ALT-003C</td>
<td class="py-3 px-4">
<div class="flex items-center gap-2">
<span class="w-2 h-2 rounded-full bg-tertiary-container"></span>
                                        Blueberries
                                    </div>
</td>
<td class="py-3 px-4">
<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-surface-variant text-on-surface-variant border border-white/10">
<span class="material-symbols-outlined text-[14px]">check_circle</span>
                                        Falsa Alarma
                                    </span>
</td>
<td class="py-3 px-4 text-center">
<div class="flex justify-center items-center gap-1 text-primary">
<span class="material-symbols-outlined text-[14px]" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-[14px]" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-[14px]" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-[14px]" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-[14px]" style="font-variation-settings: 'FILL' 1;">star</span>
</div>
</td>
<td class="py-3 px-4 text-right">3,120</td>
<td class="py-3 px-4 text-on-surface-variant">2023-10-27 13:50:11</td>
<td class="py-3 px-4 text-right">
<button class="opacity-0 group-hover:opacity-100 transition-opacity bg-primary/10 hover:bg-primary/20 text-primary border border-primary/30 px-3 py-1.5 rounded font-label-md text-label-md">
                                        Review Detail
                                    </button>
</td>
</tr>
<!-- Row 4 -->
<tr class="hover:bg-white/5 transition-colors group">
<td class="py-3 px-4">DEC-9818</td>
<td class="py-3 px-4 text-on-surface-variant">ALT-004D</td>
<td class="py-3 px-4">
<div class="flex items-center gap-2">
<span class="w-2 h-2 rounded-full bg-tertiary"></span>
                                        Avocado Hass
                                    </div>
</td>
<td class="py-3 px-4">
<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-error-container/20 text-error border border-error/30">
<span class="material-symbols-outlined text-[14px]">warning</span>
                                        Confirmed
                                    </span>
</td>
<td class="py-3 px-4 text-center">
<div class="flex justify-center items-center gap-1 text-primary">
<span class="material-symbols-outlined text-[14px]" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-[14px]" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-[14px]">star</span>
<span class="material-symbols-outlined text-[14px]">star</span>
<span class="material-symbols-outlined text-[14px]">star</span>
</div>
</td>
<td class="py-3 px-4 text-right">12,500</td>
<td class="py-3 px-4 text-on-surface-variant">2023-10-27 13:12:45</td>
<td class="py-3 px-4 text-right">
<button class="opacity-0 group-hover:opacity-100 transition-opacity bg-primary/10 hover:bg-primary/20 text-primary border border-primary/30 px-3 py-1.5 rounded font-label-md text-label-md">
                                        Review Detail
                                    </button>
</td>
</tr>
</tbody>
</table>
</div>
<!-- Pagination Footer -->
<div class="mt-auto border-t border-white/5 p-4 flex justify-between items-center bg-surface-container/20">
<span class="font-body-sm text-body-sm text-on-surface-variant">Showing 1 to 4 of 128 entries</span>
<div class="flex gap-2">
<button class="p-1 rounded hover:bg-white/10 text-on-surface-variant disabled:opacity-50" disabled="">
<span class="material-symbols-outlined">chevron_left</span>
</button>
<button class="p-1 rounded hover:bg-white/10 text-on-surface">
<span class="material-symbols-outlined">chevron_right</span>
</button>
</div>
</div>
</div>
</div>
</main>
<!-- Mobile Bottom Navigation -->
<nav class="md:hidden bg-surface-container/80 dark:bg-surface-container/80 backdrop-blur-xl border-t border-white/10 flex justify-around items-center w-full h-16 shrink-0 z-40 pb-safe">
<a class="flex flex-col items-center justify-center w-full h-full text-on-surface-variant" href="#">
<span class="material-symbols-outlined mb-1">dashboard</span>
</a>
<a class="flex flex-col items-center justify-center w-full h-full text-on-surface-variant" href="#">
<span class="material-symbols-outlined mb-1">security_update_warning</span>
</a>
<a class="flex flex-col items-center justify-center w-full h-full text-on-surface-variant" href="#">
<span class="material-symbols-outlined mb-1">monitoring</span>
</a>
<a class="flex flex-col items-center justify-center w-full h-full text-primary border-t-2 border-primary" href="#">
<span class="material-symbols-outlined mb-1" style="font-variation-settings: 'FILL' 1;">fact_check</span>
</a>
</nav>
</body></html>

<!-- Alerts Management Inbox -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Agro-Intelligence Oversight - Alerts Inbox</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Outfit:wght@400;600;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            "colors": {
                    "outline-variant": "#3f4a3f",
                    "surface-container-low": "#171d17",
                    "primary-container": "#3da35d",
                    "surface-container-lowest": "#0a100a",
                    "on-secondary-fixed-variant": "#1e502e",
                    "inverse-on-surface": "#2c322b",
                    "surface-container": "#1b211b",
                    "surface-variant": "#30362f",
                    "surface-container-highest": "#30362f",
                    "inverse-primary": "#006d33",
                    "primary-fixed": "#92f8a9",
                    "on-surface-variant": "#becabc",
                    "tertiary-fixed-dim": "#89ceff",
                    "on-surface": "#dee4da",
                    "surface-tint": "#76db8f",
                    "tertiary-fixed": "#c9e6ff",
                    "on-error-container": "#ffdad6",
                    "on-tertiary-fixed": "#001e2f",
                    "on-background": "#dee4da",
                    "on-tertiary-fixed-variant": "#004c6e",
                    "error-container": "#93000a",
                    "secondary-container": "#205331",
                    "primary-fixed-dim": "#76db8f",
                    "on-secondary-container": "#8fc599",
                    "on-primary-container": "#003114",
                    "tertiary": "#89ceff",
                    "surface-bright": "#343b34",
                    "secondary": "#9dd3a7",
                    "on-primary-fixed": "#00210b",
                    "on-tertiary": "#00344d",
                    "on-primary": "#003918",
                    "secondary-fixed": "#b8f0c2",
                    "background": "#0f150f",
                    "outline": "#889487",
                    "tertiary-container": "#009ada",
                    "primary": "#76db8f",
                    "on-tertiary-container": "#002d43",
                    "surface-container-high": "#252c25",
                    "surface-dim": "#0f150f",
                    "on-error": "#690005",
                    "inverse-surface": "#dee4da",
                    "surface": "#0f150f",
                    "on-secondary-fixed": "#00210c",
                    "on-primary-fixed-variant": "#005225",
                    "on-secondary": "#01391a",
                    "secondary-fixed-dim": "#9dd3a7",
                    "error": "#ffb4ab"
            },
            "borderRadius": {
                    "DEFAULT": "0.125rem",
                    "lg": "0.25rem",
                    "xl": "0.5rem",
                    "full": "0.75rem"
            },
            "spacing": {
                    "gutter": "16px",
                    "card-gap": "20px",
                    "container-padding": "24px",
                    "unit": "4px"
            },
            "fontFamily": {
                    "body-md": [
                            "Inter"
                    ],
                    "headline-sm": [
                            "Outfit"
                    ],
                    "body-sm": [
                            "Inter"
                    ],
                    "headline-md": [
                            "Outfit"
                    ],
                    "display-lg": [
                            "Outfit"
                    ],
                    "headline-lg": [
                            "Outfit"
                    ],
                    "mono-data": [
                            "monospace"
                    ],
                    "label-md": [
                            "Inter"
                    ],
                    "body-lg": [
                            "Inter"
                    ]
            },
            "fontSize": {
                    "body-md": [
                            "16px",
                            {
                                    "lineHeight": "24px",
                                    "fontWeight": "400"
                            }
                    ],
                    "headline-sm": [
                            "20px",
                            {
                                    "lineHeight": "28px",
                                    "fontWeight": "600"
                            }
                    ],
                    "body-sm": [
                            "14px",
                            {
                                    "lineHeight": "20px",
                                    "fontWeight": "400"
                            }
                    ],
                    "headline-md": [
                            "24px",
                            {
                                    "lineHeight": "32px",
                                    "fontWeight": "600"
                            }
                    ],
                    "display-lg": [
                            "48px",
                            {
                                    "lineHeight": "56px",
                                    "letterSpacing": "-0.02em",
                                    "fontWeight": "700"
                            }
                    ],
                    "headline-lg": [
                            "32px",
                            {
                                    "lineHeight": "40px",
                                    "fontWeight": "600"
                            }
                    ],
                    "mono-data": [
                            "14px",
                            {
                                    "lineHeight": "20px",
                                    "fontWeight": "500"
                            }
                    ],
                    "label-md": [
                            "12px",
                            {
                                    "lineHeight": "16px",
                                    "letterSpacing": "0.05em",
                                    "fontWeight": "600"
                            }
                    ],
                    "body-lg": [
                            "18px",
                            {
                                    "lineHeight": "28px",
                                    "fontWeight": "400"
                            }
                    ]
            }
    },
        },
      }
    </script>
<style>
        /* Base Dark-Glassmorphism Styles */
        body {
            background-color: #0c120c; /* Level 0 Background */
            color: #dee4da; /* on-surface */
        }
        
        .glass-panel {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .glass-input {
            background: transparent;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }
        
        .glass-input:focus {
            background: rgba(255, 255, 255, 0.06);
            border-color: #76db8f;
            box-shadow: 0 0 10px rgba(118, 219, 143, 0.2);
            outline: none;
        }

        .glass-button-primary {
            background-color: #76db8f;
            color: #003918;
            transition: all 0.2s ease;
        }
        
        .glass-button-primary:hover {
            background-color: #92f8a9;
            box-shadow: 0 0 15px rgba(118, 219, 143, 0.4);
        }

        .glass-button-secondary {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid #76db8f;
            color: #76db8f;
            transition: all 0.2s ease;
        }

        .glass-button-secondary:hover {
            background: rgba(118, 219, 143, 0.1);
            box-shadow: 0 0 15px rgba(118, 219, 143, 0.2);
        }
        
        /* Table Styles */
        .audit-table tr:nth-child(even) {
            background-color: rgba(255, 255, 255, 0.02);
        }
        
        .audit-table th {
            background-color: rgba(255, 255, 255, 0.06);
            border-bottom: 1px solid #76db8f;
        }

        .audit-table td {
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* Anomaly Badges */
        @keyframes pulse-border {
            0% { box-shadow: 0 0 0 0 rgba(255, 180, 171, 0.4); }
            70% { box-shadow: 0 0 0 6px rgba(255, 180, 171, 0); }
            100% { box-shadow: 0 0 0 0 rgba(255, 180, 171, 0); }
        }

        .badge-critical {
            background: rgba(147, 0, 10, 0.2);
            border: 1px solid #ffb4ab;
            color: #ffb4ab;
            animation: pulse-border 2s infinite;
        }

        .badge-high {
            background: rgba(255, 180, 171, 0.1);
            border: 1px solid #ffb4ab;
            color: #ffb4ab;
        }
        
        .badge-medium {
            background: rgba(201, 230, 255, 0.1);
            border: 1px solid #89ceff;
            color: #89ceff;
        }

        .badge-low {
            background: rgba(157, 211, 167, 0.1);
            border: 1px solid #9dd3a7;
            color: #9dd3a7;
        }

        /* Checkbox Override */
        [type="checkbox"] {
            background-color: transparent;
            border-color: rgba(255,255,255,0.3);
            border-radius: 2px;
        }
        [type="checkbox"]:checked {
            background-color: #76db8f;
            border-color: #76db8f;
        }
        [type="checkbox"]:focus {
            --tw-ring-color: #76db8f;
            --tw-ring-offset-color: #0c120c;
        }

        /* Custom Scrollbar for table container */
        .table-container::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        .table-container::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.02);
        }
        .table-container::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }
        .table-container::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.2);
        }
    </style>
</head>
<body class="font-body-md text-body-md bg-background text-on-background antialiased flex h-screen overflow-hidden">
<!-- TopNavBar (Mobile Only) -->
<nav class="md:hidden flex justify-between items-center px-container-padding w-full h-16 bg-surface-container/40 dark:bg-surface-container/40 backdrop-blur-xl fixed top-0 z-50 border-b border-white/10 shadow-sm">
<div class="font-headline-md text-headline-md font-bold text-primary">Agro-Intelligence Oversight</div>
<div class="flex gap-4">
<span class="material-symbols-outlined text-on-surface-variant cursor-pointer active:scale-95" data-icon="notifications">notifications</span>
<span class="material-symbols-outlined text-on-surface-variant cursor-pointer active:scale-95" data-icon="settings">settings</span>
</div>
</nav>
<!-- SideNavBar (Desktop) -->
<nav class="hidden md:flex flex-col py-6 h-full h-screen w-20 hover:w-64 transition-all duration-300 ease-in-out fixed left-0 top-0 z-50 bg-surface-container-lowest dark:bg-surface-container-lowest border-r border-white/5 shadow-2xl group overflow-hidden">
<div class="flex items-center px-6 mb-8 whitespace-nowrap">
<span class="material-symbols-outlined text-primary-fixed text-[32px] shrink-0" data-icon="radar">radar</span>
<div class="ml-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
<div class="font-headline-sm text-headline-sm text-primary-fixed">AUDIT_OS_V1</div>
<div class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Terminal Active</div>
</div>
</div>
<div class="flex-1 flex flex-col gap-2 w-full px-2">
<a class="flex items-center px-4 py-3 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg transition-colors whitespace-nowrap" href="#">
<span class="material-symbols-outlined shrink-0" data-icon="dashboard">dashboard</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300">Dashboard</span>
</a>
<a class="flex items-center px-4 py-3 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg transition-colors whitespace-nowrap" href="#">
<span class="material-symbols-outlined shrink-0" data-icon="security_update_warning">security_update_warning</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300">Risk Analysis</span>
</a>
<a class="flex items-center px-4 py-3 bg-primary-container text-on-primary-container rounded-lg mx-2 transition-colors whitespace-nowrap" href="#">
<span class="material-symbols-outlined shrink-0" data-icon="monitoring">monitoring</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300">Telemetry</span>
</a>
<a class="flex items-center px-4 py-3 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg transition-colors whitespace-nowrap" href="#">
<span class="material-symbols-outlined shrink-0" data-icon="fact_check">fact_check</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300">Audits</span>
</a>
<a class="flex items-center px-4 py-3 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg transition-colors whitespace-nowrap" href="#">
<span class="material-symbols-outlined shrink-0" data-icon="settings">settings</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300">Settings</span>
</a>
</div>
<div class="px-4 mb-4 whitespace-nowrap">
<button class="w-full flex items-center justify-center py-2 px-4 glass-button-secondary rounded-lg font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300">
<span class="material-symbols-outlined mr-2 text-[18px]">download</span> Export Report
            </button>
</div>
<div class="flex flex-col gap-2 w-full px-2 border-t border-white/5 pt-4">
<a class="flex items-center px-4 py-2 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg transition-colors whitespace-nowrap" href="#">
<span class="material-symbols-outlined shrink-0 text-[20px]" data-icon="help">help</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300">Support</span>
</a>
<a class="flex items-center px-4 py-2 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg transition-colors whitespace-nowrap" href="#">
<span class="material-symbols-outlined shrink-0 text-[20px]" data-icon="logout">logout</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300">Logout</span>
</a>
</div>
</nav>
<!-- Main Content Canvas -->
<main class="flex-1 md:ml-20 mt-16 md:mt-0 p-container-padding flex flex-col h-full overflow-hidden relative z-10 transition-all duration-300">
<!-- Header -->
<header class="flex flex-col md:flex-row md:items-end justify-between mb-card-gap shrink-0 gap-4">
<div>
<h1 class="font-headline-lg text-headline-lg text-on-surface mb-1">Telemetry Alerts Inbox</h1>
<p class="font-body-md text-body-md text-on-surface-variant">Monitoring real-time deviations in agro-export data streams.</p>
</div>
<div class="flex gap-3">
<button class="glass-button-secondary px-4 py-2 rounded-DEFAULT font-label-md text-label-md flex items-center gap-2">
<span class="material-symbols-outlined text-[18px]">rule</span> Bulk Assign
                </button>
<button class="glass-button-primary px-4 py-2 rounded-DEFAULT font-label-md text-label-md font-semibold flex items-center gap-2">
<span class="material-symbols-outlined text-[18px]">refresh</span> Sync Data
                </button>
</div>
</header>
<!-- Advanced Filter Bar (Glass Panel) -->
<section class="glass-panel rounded-xl p-4 mb-card-gap shrink-0 flex flex-col lg:flex-row gap-4 items-center">
<!-- Search Input -->
<div class="relative w-full lg:w-1/3">
<span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-outline">search</span>
<input class="glass-input w-full pl-10 pr-4 py-2 rounded-DEFAULT font-body-sm text-body-sm text-on-surface placeholder:text-outline-variant focus:ring-0" placeholder="Search ID / DAM / RUC..." type="text"/>
</div>
<div class="flex flex-wrap md:flex-nowrap gap-4 w-full lg:w-2/3">
<!-- Product Filter -->
<div class="flex-1 min-w-[120px]">
<select class="glass-input w-full px-3 py-2 rounded-DEFAULT font-body-sm text-body-sm text-on-surface appearance-none focus:ring-0">
<option class="bg-surface-container text-on-surface" value="">Product: All</option>
<option class="bg-surface-container text-on-surface" value="palta">Palta</option>
<option class="bg-surface-container text-on-surface" value="uva">Uva</option>
<option class="bg-surface-container text-on-surface" value="arandano">Arándano</option>
<option class="bg-surface-container text-on-surface" value="mango">Mango</option>
</select>
</div>
<!-- Severity Filter -->
<div class="flex-1 min-w-[120px]">
<select class="glass-input w-full px-3 py-2 rounded-DEFAULT font-body-sm text-body-sm text-on-surface appearance-none focus:ring-0">
<option class="bg-surface-container text-on-surface" value="">Severity: All</option>
<option class="bg-surface-container text-on-surface" value="critical">Critical</option>
<option class="bg-surface-container text-on-surface" value="high">High</option>
<option class="bg-surface-container text-on-surface" value="medium">Medium</option>
<option class="bg-surface-container text-on-surface" value="low">Low</option>
</select>
</div>
<!-- Status Filter -->
<div class="flex-1 min-w-[120px]">
<select class="glass-input w-full px-3 py-2 rounded-DEFAULT font-body-sm text-body-sm text-on-surface appearance-none focus:ring-0">
<option class="bg-surface-container text-on-surface" value="">Status: All</option>
<option class="bg-surface-container text-on-surface" value="pending">Pending</option>
<option class="bg-surface-container text-on-surface" value="review">In Review</option>
<option class="bg-surface-container text-on-surface" value="confirmed">Confirmed</option>
<option class="bg-surface-container text-on-surface" value="discarded">Discarded</option>
</select>
</div>
</div>
<button class="shrink-0 p-2 text-on-surface-variant hover:text-primary transition-colors" title="Clear Filters">
<span class="material-symbols-outlined">filter_alt_off</span>
</button>
</section>
<!-- Data Table Container -->
<section class="glass-panel rounded-xl flex-1 flex flex-col overflow-hidden relative">
<div class="table-container overflow-auto flex-1">
<table class="w-full text-left border-collapse audit-table whitespace-nowrap">
<thead class="sticky top-0 z-10 font-label-md text-label-md text-on-surface uppercase tracking-wider">
<tr>
<th class="px-4 py-3 w-12 text-center"><input class="rounded-sm" type="checkbox"/></th>
<th class="px-4 py-3">Alert ID</th>
<th class="px-4 py-3">DAM</th>
<th class="px-4 py-3">Date/Time</th>
<th class="px-4 py-3">Product</th>
<th class="px-4 py-3">Exportadora</th>
<th class="px-4 py-3">Destination</th>
<th class="px-4 py-3 text-right">FOB Value</th>
<th class="px-4 py-3 text-right">Dev %</th>
<th class="px-4 py-3 text-center">Score</th>
<th class="px-4 py-3 text-center">Severity</th>
<th class="px-4 py-3 text-center">Status</th>
<th class="px-4 py-3 w-12"></th>
</tr>
</thead>
<tbody class="font-mono-data text-mono-data text-on-surface-variant">
<!-- Row 1: Critical -->
<tr class="hover:bg-white/5 transition-colors group cursor-pointer">
<td class="px-4 py-3 text-center"><input class="rounded-sm" type="checkbox"/></td>
<td class="px-4 py-3 text-primary font-bold">ALT-8892</td>
<td class="px-4 py-3">118-2023-10-123456</td>
<td class="px-4 py-3 text-body-sm font-body-sm">2023-10-25 14:32:01</td>
<td class="px-4 py-3"><span class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-[#5d8a3e]"></span>Palta Hass</span></td>
<td class="px-4 py-3 font-body-sm font-body-sm truncate max-w-[150px]">AGRO EXPORTACIONES S.A.C.</td>
<td class="px-4 py-3">Rotterdam (NLRTM)</td>
<td class="px-4 py-3 text-right">$ 145,200.00</td>
<td class="px-4 py-3 text-right text-error">+45.2%</td>
<td class="px-4 py-3 text-center">98.5</td>
<td class="px-4 py-3 text-center">
<span class="badge-critical px-2 py-1 rounded-DEFAULT font-label-md text-[10px] uppercase inline-flex items-center gap-1">
<span class="material-symbols-outlined text-[14px]">warning</span> Critical
                                </span>
</td>
<td class="px-4 py-3 text-center">
<span class="text-error-container border border-error-container bg-error-container/10 px-2 py-1 rounded-DEFAULT font-label-md text-[10px] uppercase">Pending</span>
</td>
<td class="px-4 py-3 text-center">
<button class="text-outline hover:text-primary transition-colors opacity-0 group-hover:opacity-100"><span class="material-symbols-outlined">chevron_right</span></button>
</td>
</tr>
<!-- Row 2: High -->
<tr class="hover:bg-white/5 transition-colors group cursor-pointer">
<td class="px-4 py-3 text-center"><input class="rounded-sm" type="checkbox"/></td>
<td class="px-4 py-3 text-primary font-bold">ALT-8891</td>
<td class="px-4 py-3">118-2023-10-123412</td>
<td class="px-4 py-3 text-body-sm font-body-sm">2023-10-25 13:15:44</td>
<td class="px-4 py-3"><span class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-[#8b3a62]"></span>Uva Red Globe</span></td>
<td class="px-4 py-3 font-body-sm font-body-sm truncate max-w-[150px]">FRUTOS DEL SUR E.I.R.L.</td>
<td class="px-4 py-3">Shanghai (CNSHA)</td>
<td class="px-4 py-3 text-right">$ 89,500.00</td>
<td class="px-4 py-3 text-right text-[#ffb4ab]">-28.4%</td>
<td class="px-4 py-3 text-center">82.1</td>
<td class="px-4 py-3 text-center">
<span class="badge-high px-2 py-1 rounded-DEFAULT font-label-md text-[10px] uppercase inline-flex items-center gap-1">
<span class="material-symbols-outlined text-[14px]">priority_high</span> High
                                </span>
</td>
<td class="px-4 py-3 text-center">
<span class="text-tertiary border border-tertiary bg-tertiary/10 px-2 py-1 rounded-DEFAULT font-label-md text-[10px] uppercase">Review</span>
</td>
<td class="px-4 py-3 text-center">
<button class="text-outline hover:text-primary transition-colors opacity-0 group-hover:opacity-100"><span class="material-symbols-outlined">chevron_right</span></button>
</td>
</tr>
<!-- Row 3: Medium -->
<tr class="hover:bg-white/5 transition-colors group cursor-pointer">
<td class="px-4 py-3 text-center"><input class="rounded-sm" type="checkbox"/></td>
<td class="px-4 py-3 text-primary font-bold">ALT-8890</td>
<td class="px-4 py-3">084-2023-10-098765</td>
<td class="px-4 py-3 text-body-sm font-body-sm">2023-10-25 11:05:22</td>
<td class="px-4 py-3"><span class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-[#3b5998]"></span>Arándano</span></td>
<td class="px-4 py-3 font-body-sm font-body-sm truncate max-w-[150px]">BERRIES DEL NORTE S.A.</td>
<td class="px-4 py-3">Philadelphia (USPHL)</td>
<td class="px-4 py-3 text-right">$ 210,000.00</td>
<td class="px-4 py-3 text-right text-[#89ceff]">+15.8%</td>
<td class="px-4 py-3 text-center">64.3</td>
<td class="px-4 py-3 text-center">
<span class="badge-medium px-2 py-1 rounded-DEFAULT font-label-md text-[10px] uppercase inline-flex items-center gap-1">
<span class="material-symbols-outlined text-[14px]">info</span> Medium
                                </span>
</td>
<td class="px-4 py-3 text-center">
<span class="text-primary border border-primary bg-primary/10 px-2 py-1 rounded-DEFAULT font-label-md text-[10px] uppercase">Confirmed</span>
</td>
<td class="px-4 py-3 text-center">
<button class="text-outline hover:text-primary transition-colors opacity-0 group-hover:opacity-100"><span class="material-symbols-outlined">chevron_right</span></button>
</td>
</tr>
<!-- Row 4: Low -->
<tr class="hover:bg-white/5 transition-colors group cursor-pointer opacity-70 hover:opacity-100">
<td class="px-4 py-3 text-center"><input class="rounded-sm" type="checkbox"/></td>
<td class="px-4 py-3 text-primary font-bold">ALT-8889</td>
<td class="px-4 py-3">118-2023-10-123399</td>
<td class="px-4 py-3 text-body-sm font-body-sm">2023-10-25 09:44:10</td>
<td class="px-4 py-3"><span class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-[#f4a460]"></span>Mango Kent</span></td>
<td class="px-4 py-3 font-body-sm font-body-sm truncate max-w-[150px]">TROPICAL EXPORTS LLC</td>
<td class="px-4 py-3">Algeciras (ESALG)</td>
<td class="px-4 py-3 text-right">$ 42,300.00</td>
<td class="px-4 py-3 text-right text-[#9dd3a7]">-5.2%</td>
<td class="px-4 py-3 text-center">31.0</td>
<td class="px-4 py-3 text-center">
<span class="badge-low px-2 py-1 rounded-DEFAULT font-label-md text-[10px] uppercase inline-flex items-center gap-1">
<span class="material-symbols-outlined text-[14px]">check_circle</span> Low
                                </span>
</td>
<td class="px-4 py-3 text-center">
<span class="text-outline border border-outline bg-outline/10 px-2 py-1 rounded-DEFAULT font-label-md text-[10px] uppercase">Discarded</span>
</td>
<td class="px-4 py-3 text-center">
<button class="text-outline hover:text-primary transition-colors opacity-0 group-hover:opacity-100"><span class="material-symbols-outlined">chevron_right</span></button>
</td>
</tr>
</tbody>
</table>
<!-- Loading State (Hidden by default, shown for demonstration) -->
<!-- 
                <div class="w-full flex flex-col items-center justify-center py-12 text-outline">
                    <span class="material-symbols-outlined text-[48px] animate-spin mb-4">autorenew</span>
                    <p class="font-body-md text-body-md">Ingesting Telemetry Data...</p>
                </div>
                -->
<!-- Empty State (Hidden by default) -->
<!--
                <div class="w-full flex flex-col items-center justify-center py-16 text-outline">
                    <span class="material-symbols-outlined text-[64px] mb-4 opacity-50">data_alert</span>
                    <p class="font-headline-sm text-headline-sm text-on-surface mb-2">No anomalies detected</p>
                    <p class="font-body-md text-body-md text-center max-w-md">The current data stream parameters match historical baselines. Adjust filters to search past events.</p>
                </div>
                -->
</div>
<!-- Table Footer / Pagination -->
<div class="border-t border-white/5 p-4 flex justify-between items-center bg-surface-container-low shrink-0">
<div class="font-body-sm text-body-sm text-on-surface-variant">
                    Showing <span class="text-on-surface font-semibold">1</span> to <span class="text-on-surface font-semibold">4</span> of <span class="text-on-surface font-semibold">1,248</span> alerts
                </div>
<div class="flex gap-2">
<button class="px-3 py-1 glass-panel rounded-DEFAULT text-outline hover:text-primary hover:border-primary disabled:opacity-50 disabled:cursor-not-allowed transition-colors" disabled="">
<span class="material-symbols-outlined text-[20px]">chevron_left</span>
</button>
<button class="px-3 py-1 glass-panel rounded-DEFAULT text-primary border-primary bg-primary/10 font-mono-data text-mono-data">1</button>
<button class="px-3 py-1 glass-panel rounded-DEFAULT text-on-surface-variant hover:text-primary hover:border-primary font-mono-data text-mono-data transition-colors">2</button>
<button class="px-3 py-1 glass-panel rounded-DEFAULT text-on-surface-variant hover:text-primary hover:border-primary font-mono-data text-mono-data transition-colors">3</button>
<span class="px-2 py-1 text-on-surface-variant">...</span>
<button class="px-3 py-1 glass-panel rounded-DEFAULT text-on-surface-variant hover:text-primary hover:border-primary transition-colors">
<span class="material-symbols-outlined text-[20px]">chevron_right</span>
</button>
</div>
</div>
</section>
</main>
<!-- Simulated Quick View Drawer (Hidden by default, shown via CSS for demonstration purposes here, normally triggered via JS) -->
<!-- Add a class like 'translate-x-full' to hide it normally -->
<aside class="fixed inset-y-0 right-0 w-full md:w-[450px] bg-surface-container-highest/95 backdrop-blur-3xl border-l border-white/10 shadow-[-10px_0_30px_rgba(0,0,0,0.5)] z-50 transform translate-x-full transition-transform duration-300 ease-in-out flex flex-col" id="quick-view-drawer">
<div class="p-6 border-b border-white/10 flex justify-between items-start">
<div>
<div class="flex items-center gap-3 mb-2">
<h2 class="font-headline-md text-headline-md text-primary font-bold">ALT-8892</h2>
<span class="badge-critical px-2 py-1 rounded-DEFAULT font-label-md text-[10px] uppercase">Critical</span>
</div>
<p class="font-mono-data text-mono-data text-on-surface-variant">DAM: 118-2023-10-123456</p>
</div>
<button class="text-outline hover:text-primary transition-colors" onclick="document.getElementById('quick-view-drawer').classList.add('translate-x-full')">
<span class="material-symbols-outlined">close</span>
</button>
</div>
<div class="p-6 overflow-y-auto flex-1 flex flex-col gap-6">
<!-- Anomaly Summary -->
<div class="glass-panel p-4 rounded-xl">
<h3 class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-4 border-b border-white/10 pb-2">Deviation Signature</h3>
<div class="grid grid-cols-2 gap-4">
<div>
<p class="font-body-sm text-body-sm text-outline">Expected FOB Value</p>
<p class="font-mono-data text-mono-data text-on-surface">$ 100,000.00</p>
</div>
<div>
<p class="font-body-sm text-body-sm text-outline">Declared FOB Value</p>
<p class="font-mono-data text-mono-data text-error font-bold">$ 145,200.00</p>
</div>
<div class="col-span-2">
<div class="w-full bg-surface-container h-2 rounded-full overflow-hidden mt-2">
<div class="bg-error h-full" style="width: 45.2%"></div>
</div>
<p class="font-label-md text-label-md text-error mt-1 text-right">+45.2% Overvaluation</p>
</div>
</div>
</div>
<!-- Context Data -->
<div>
<h3 class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-4 border-b border-white/10 pb-2">Entity Context</h3>
<dl class="space-y-3 font-body-sm text-body-sm">
<div class="flex justify-between">
<dt class="text-outline">Exportadora</dt>
<dd class="text-on-surface font-medium text-right max-w-[200px] truncate">AGRO EXPORTACIONES S.A.C.</dd>
</div>
<div class="flex justify-between">
<dt class="text-outline">RUC</dt>
<dd class="font-mono-data text-mono-data text-on-surface">20512345678</dd>
</div>
<div class="flex justify-between">
<dt class="text-outline">Product Profile</dt>
<dd class="text-on-surface">Palta Hass (Fresh)</dd>
</div>
<div class="flex justify-between">
<dt class="text-outline">Destination</dt>
<dd class="text-on-surface">Rotterdam, Netherlands</dd>
</div>
<div class="flex justify-between">
<dt class="text-outline">Risk Profile</dt>
<dd class="text-[#ffb4ab]">High (Prior Infractions: 2)</dd>
</div>
</dl>
</div>
<!-- Action Area -->
<div class="mt-auto pt-6 border-t border-white/10">
<label class="block font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-2">Update Status</label>
<select class="glass-input w-full px-3 py-2 rounded-DEFAULT font-body-sm text-body-sm text-on-surface appearance-none mb-4">
<option class="bg-surface-container text-on-surface" value="pending">Pending</option>
<option class="bg-surface-container text-on-surface" value="review">In Review (Assigning to self)</option>
<option class="bg-surface-container text-on-surface" value="confirmed">Confirmed (Send to Fiscalización)</option>
<option class="bg-surface-container text-on-surface" value="discarded">Discarded (False Positive)</option>
</select>
<textarea class="glass-input w-full p-3 rounded-DEFAULT font-body-sm text-body-sm text-on-surface placeholder:text-outline-variant mb-4 h-24" placeholder="Add auditor notes..."></textarea>
<div class="flex gap-3">
<button class="flex-1 glass-button-secondary py-2 rounded-DEFAULT font-label-md text-label-md">Cancel</button>
<button class="flex-1 glass-button-primary py-2 rounded-DEFAULT font-label-md text-label-md font-semibold">Save Decision</button>
</div>
</div>
</div>
</aside>
<script>
        // Simple script to demonstrate drawer opening from table row click
        document.querySelectorAll('.audit-table tbody tr').forEach(row => {
            row.addEventListener('click', (e) => {
                // Prevent opening if clicking on checkbox
                if(e.target.tagName !== 'INPUT') {
                    document.getElementById('quick-view-drawer').classList.remove('translate-x-full');
                }
            });
        });
    </script>
</body></html>

<!-- Data Explorer & Load Center -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Agro-Intelligence Oversight - Data Explorer</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&amp;family=Outfit:wght@600;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    "colors": {
                        "outline-variant": "#3f4a3f",
                        "surface-container-low": "#171d17",
                        "primary-container": "#3da35d",
                        "surface-container-lowest": "#0a100a",
                        "on-secondary-fixed-variant": "#1e502e",
                        "inverse-on-surface": "#2c322b",
                        "surface-container": "#1b211b",
                        "surface-variant": "#30362f",
                        "surface-container-highest": "#30362f",
                        "inverse-primary": "#006d33",
                        "primary-fixed": "#92f8a9",
                        "on-surface-variant": "#becabc",
                        "tertiary-fixed-dim": "#89ceff",
                        "on-surface": "#dee4da",
                        "surface-tint": "#76db8f",
                        "tertiary-fixed": "#c9e6ff",
                        "on-error-container": "#ffdad6",
                        "on-tertiary-fixed": "#001e2f",
                        "on-background": "#dee4da",
                        "on-tertiary-fixed-variant": "#004c6e",
                        "error-container": "#93000a",
                        "secondary-container": "#205331",
                        "primary-fixed-dim": "#76db8f",
                        "on-secondary-container": "#8fc599",
                        "on-primary-container": "#003114",
                        "tertiary": "#89ceff",
                        "surface-bright": "#343b34",
                        "secondary": "#9dd3a7",
                        "on-primary-fixed": "#00210b",
                        "on-tertiary": "#00344d",
                        "on-primary": "#003918",
                        "secondary-fixed": "#b8f0c2",
                        "background": "#0f150f",
                        "outline": "#889487",
                        "tertiary-container": "#009ada",
                        "primary": "#76db8f",
                        "on-tertiary-container": "#002d43",
                        "surface-container-high": "#252c25",
                        "surface-dim": "#0f150f",
                        "on-error": "#690005",
                        "inverse-surface": "#dee4da",
                        "surface": "#0f150f",
                        "on-secondary-fixed": "#00210c",
                        "on-primary-fixed-variant": "#005225",
                        "on-secondary": "#01391a",
                        "secondary-fixed-dim": "#9dd3a7",
                        "error": "#ffb4ab"
                    },
                    "borderRadius": {
                        "DEFAULT": "0.125rem",
                        "lg": "0.25rem",
                        "xl": "0.5rem",
                        "full": "0.75rem"
                    },
                    "spacing": {
                        "gutter": "16px",
                        "card-gap": "20px",
                        "container-padding": "24px",
                        "unit": "4px"
                    },
                    "fontFamily": {
                        "body-md": ["Inter"],
                        "headline-sm": ["Outfit"],
                        "body-sm": ["Inter"],
                        "headline-md": ["Outfit"],
                        "display-lg": ["Outfit"],
                        "headline-lg": ["Outfit"],
                        "mono-data": ["monospace"],
                        "label-md": ["Inter"],
                        "body-lg": ["Inter"]
                    },
                    "fontSize": {
                        "body-md": ["16px", {"lineHeight": "24px", "fontWeight": "400"}],
                        "headline-sm": ["20px", {"lineHeight": "28px", "fontWeight": "600"}],
                        "body-sm": ["14px", {"lineHeight": "20px", "fontWeight": "400"}],
                        "headline-md": ["24px", {"lineHeight": "32px", "fontWeight": "600"}],
                        "display-lg": ["48px", {"lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "700"}],
                        "headline-lg": ["32px", {"lineHeight": "40px", "fontWeight": "600"}],
                        "mono-data": ["14px", {"lineHeight": "20px", "fontWeight": "500"}],
                        "label-md": ["12px", {"lineHeight": "16px", "letterSpacing": "0.05em", "fontWeight": "600"}],
                        "body-lg": ["18px", {"lineHeight": "28px", "fontWeight": "400"}]
                    }
                }
            }
        }
    </script>
<style>
        body {
            background-color: #0f150f;
            color: #dee4da;
        }
        .glass-panel {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .glass-panel-hover:hover {
            background: rgba(255, 255, 255, 0.06);
            border-color: rgba(118, 219, 143, 0.5); /* Primary tint */
        }
        .glass-input {
            background: transparent;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
        }
        .glass-input:focus {
            background: rgba(255, 255, 255, 0.05);
            border-color: #76db8f;
            outline: none;
            box-shadow: 0 0 0 1px #76db8f;
        }
        .drag-active {
            border-color: #76db8f;
            background: rgba(118, 219, 143, 0.1);
        }
        /* Custom Scrollbar for tables */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0f150f; 
        }
        ::-webkit-scrollbar-thumb {
            background: #30362f; 
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #3f4a3f; 
        }
    </style>
</head>
<body class="flex h-screen overflow-hidden antialiased">
<!-- SideNavBar -->
<nav class="h-screen w-20 hover:w-64 transition-all duration-300 ease-in-out fixed left-0 top-0 z-50 bg-surface-container-lowest dark:bg-surface-container-lowest text-primary font-label-md text-label-md uppercase tracking-wider border-r border-white/5 shadow-2xl flex flex-col py-6 h-full group">
<div class="flex items-center px-4 mb-8 overflow-hidden whitespace-nowrap">
<div class="w-10 h-10 rounded-full bg-surface-variant flex items-center justify-center shrink-0">
<span class="material-symbols-outlined text-primary">terminal</span>
</div>
<div class="ml-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
<div class="font-headline-sm text-headline-sm text-primary-fixed">AUDIT_OS_V1</div>
<div class="text-on-surface-variant text-[10px] mt-1">Terminal Active</div>
</div>
</div>
<div class="flex-1 overflow-y-auto overflow-x-hidden">
<ul class="space-y-2">
<li>
<a class="flex items-center px-4 py-3 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg transition-colors" href="#">
<span class="material-symbols-outlined shrink-0" style="font-variation-settings: 'FILL' 0;">dashboard</span>
<span class="ml-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Dashboard</span>
</a>
</li>
<li>
<a class="flex items-center px-4 py-3 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg transition-colors" href="#">
<span class="material-symbols-outlined shrink-0" style="font-variation-settings: 'FILL' 0;">security_update_warning</span>
<span class="ml-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Risk Analysis</span>
</a>
</li>
<!-- Active Item: Telemetry closely aligns with Data Explorer / Datasets -->
<li>
<a class="flex items-center px-4 py-3 bg-primary-container text-on-primary-container rounded-lg mx-2 transition-colors" href="#">
<span class="material-symbols-outlined shrink-0" style="font-variation-settings: 'FILL' 1;">monitoring</span>
<span class="ml-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Telemetry</span>
</a>
</li>
<li>
<a class="flex items-center px-4 py-3 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg transition-colors" href="#">
<span class="material-symbols-outlined shrink-0" style="font-variation-settings: 'FILL' 0;">fact_check</span>
<span class="ml-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Audits</span>
</a>
</li>
<li>
<a class="flex items-center px-4 py-3 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg transition-colors" href="#">
<span class="material-symbols-outlined shrink-0" style="font-variation-settings: 'FILL' 0;">settings</span>
<span class="ml-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Settings</span>
</a>
</li>
</ul>
</div>
<div class="mt-auto px-4 mb-4">
<button class="w-full flex items-center justify-center py-2 px-4 rounded bg-primary/10 text-primary border border-primary/30 hover:bg-primary/20 transition-colors opacity-0 group-hover:opacity-100 whitespace-nowrap">
<span class="material-symbols-outlined text-[18px] mr-2">download</span>
                Export Report
            </button>
</div>
<ul class="space-y-2 border-t border-white/5 pt-4">
<li>
<a class="flex items-center px-4 py-2 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg transition-colors" href="#">
<span class="material-symbols-outlined shrink-0 text-[20px]" style="font-variation-settings: 'FILL' 0;">help</span>
<span class="ml-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Support</span>
</a>
</li>
<li>
<a class="flex items-center px-4 py-2 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg transition-colors" href="#">
<span class="material-symbols-outlined shrink-0 text-[20px]" style="font-variation-settings: 'FILL' 0;">logout</span>
<span class="ml-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Logout</span>
</a>
</li>
</ul>
</nav>
<!-- Main Content Area -->
<main class="flex-1 ml-20 flex flex-col overflow-hidden relative">
<!-- Subtle Ambient Background -->
<div class="absolute top-[-10%] right-[-10%] w-[600px] h-[600px] bg-primary/5 rounded-full blur-[120px] pointer-events-none"></div>
<!-- TopNavBar -->
<header class="bg-surface-container/40 dark:bg-surface-container/40 backdrop-blur-xl text-primary font-body-md text-body-md docked full-width top-0 border-b border-white/10 shadow-sm flex justify-between items-center px-container-padding w-full h-16 z-40 relative">
<div class="flex items-center space-x-8">
<div class="font-headline-md text-headline-md font-bold text-primary mr-8 tracking-tight">Agro-Intelligence Oversight</div>
<nav class="hidden md:flex space-x-6">
<!-- Active Link -->
<a class="text-primary border-b-2 border-primary pb-1 cursor-pointer active:scale-95 hover:text-primary transition-colors" href="#">Telemetry</a>
<a class="text-on-surface-variant cursor-pointer active:scale-95 hover:text-primary transition-colors pb-1" href="#">Audits</a>
<a class="text-on-surface-variant cursor-pointer active:scale-95 hover:text-primary transition-colors pb-1" href="#">Inventory</a>
</nav>
</div>
<div class="flex items-center space-x-4">
<div class="relative hidden sm:block">
<span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-[20px]">search</span>
<input class="glass-input pl-10 pr-4 py-1.5 rounded-full text-body-sm font-body-sm text-on-surface w-64 placeholder-on-surface-variant focus:w-72 transition-all duration-300" placeholder="Search datasets..." type="text"/>
</div>
<button class="p-2 text-on-surface-variant hover:text-primary transition-colors rounded-full hover:bg-surface-variant/50">
<span class="material-symbols-outlined">notifications</span>
</button>
<button class="p-2 text-on-surface-variant hover:text-primary transition-colors rounded-full hover:bg-surface-variant/50">
<span class="material-symbols-outlined">settings</span>
</button>
<div class="w-8 h-8 rounded-full bg-surface-variant border border-primary/20 overflow-hidden cursor-pointer ml-2">
<!-- Image Placeholder for Auditor Profile -->
<img alt="Auditor Profile" class="w-full h-full object-cover" data-alt="A macro shot of an advanced, dark-glassmorphism digital ID badge. The badge displays a sharp, high-contrast abstract geometric avatar against a deep charcoal-green background. Subtle, luminous emerald green data lines intersect across the surface, implying a high-tech, precision-focused environment. High-key white lighting provides a bright, modern specular reflection on the glass surface." src="https://lh3.googleusercontent.com/aida-public/AB6AXuA1oBtPm5K21gjIvYsQgEuVenraPCtl4s1vsZ8g1YlcCOAr5GglBvU85lQhCN9MnmT84ogWkl4pElDf2y2UKpGYa4N0eG97B8uaea1QwyrLbu_rd25965RT5x3gPyiSKagfFdsRnFrY6RzFvFtm2WWS1F_BbIckrPZ5QSt44B9HChPKaTXYVN_0uDWoxM26yOgdrA0qdNexKHjRHeCmJZqGaXo7AmVV-G0lrc8nJdTajE02t-oOdK4Kv-OD4x3tWwVrofSpVNxdMmc"/>
</div>
</div>
</header>
<!-- Scrollable Canvas -->
<div class="flex-1 overflow-y-auto p-container-padding z-10 relative">
<div class="max-w-7xl mx-auto space-y-card-gap">
<!-- Page Header -->
<div class="flex justify-between items-end mb-8">
<div>
<h1 class="font-headline-lg text-headline-lg text-on-surface">Data Explorer</h1>
<p class="font-body-md text-body-md text-on-surface-variant mt-1">Manage and ingest telemetry datasets for agro-industrial analysis.</p>
</div>
</div>
<!-- KPI Bento Grid -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-card-gap">
<!-- KPI 1 -->
<div class="glass-panel rounded-xl p-6 relative overflow-hidden group">
<div class="absolute right-0 bottom-0 opacity-10">
<span class="material-symbols-outlined text-[100px]" style="font-variation-settings: 'FILL' 1;">dataset</span>
</div>
<div class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-2">Total Datasets</div>
<div class="font-display-lg text-display-lg text-primary">12</div>
<div class="mt-4 flex items-center text-primary text-sm">
<span class="material-symbols-outlined text-[16px] mr-1">trending_up</span>
<span>+2 this week</span>
</div>
</div>
<!-- KPI 2 -->
<div class="glass-panel rounded-xl p-6 relative overflow-hidden">
<div class="absolute right-0 bottom-0 opacity-10">
<span class="material-symbols-outlined text-[100px]" style="font-variation-settings: 'FILL' 1;">table_rows</span>
</div>
<div class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-2">Total Records</div>
<div class="font-display-lg text-display-lg text-on-surface">1.2M</div>
<div class="mt-4 flex items-center text-on-surface-variant text-sm">
<span class="material-symbols-outlined text-[16px] mr-1">check_circle</span>
<span>Validated via OS</span>
</div>
</div>
<!-- KPI 3 -->
<div class="glass-panel rounded-xl p-6 relative overflow-hidden">
<div class="absolute right-0 bottom-0 opacity-10">
<span class="material-symbols-outlined text-[100px]" style="font-variation-settings: 'FILL' 1;">sync</span>
</div>
<div class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-2">Last Sync</div>
<div class="font-display-lg text-display-lg text-on-surface">Just Now</div>
<div class="mt-4 flex items-center text-primary text-sm">
<span class="flex h-2 w-2 rounded-full bg-primary mr-2 shadow-[0_0_8px_#76db8f] animate-pulse"></span>
<span>Live Telemetry Active</span>
</div>
</div>
</div>
<!-- Main Content Layout -->
<div class="grid grid-cols-1 lg:grid-cols-3 gap-card-gap">
<!-- Left Column: Datasets & Upload -->
<div class="lg:col-span-1 flex flex-col space-y-card-gap">
<!-- Upload Zone -->
<div class="glass-panel rounded-xl p-6 flex flex-col">
<h2 class="font-headline-sm text-headline-sm text-on-surface mb-4">Ingest Data</h2>
<div class="border-2 border-dashed border-outline-variant rounded-lg p-8 flex flex-col items-center justify-center text-center transition-all duration-300 hover:border-primary/50 hover:bg-primary/5 cursor-pointer" id="dropzone">
<span class="material-symbols-outlined text-4xl text-on-surface-variant mb-3">cloud_upload</span>
<div class="font-body-md text-body-md text-on-surface mb-1">Drag &amp; Drop CSV/XLSX</div>
<div class="font-body-sm text-body-sm text-on-surface-variant mb-4">Max file size 15MB</div>
<button class="px-4 py-2 bg-primary/10 text-primary border border-primary/30 rounded-lg hover:bg-primary/20 transition-colors font-label-md text-label-md">
                                    Browse Files
                                </button>
</div>
<!-- Mock Progress Bar (Hidden by default, shown for UI demonstration) -->
<div class="mt-4 pt-4 border-t border-white/5">
<div class="flex justify-between items-center mb-1">
<span class="font-body-sm text-body-sm text-on-surface">midagri_export_q3.csv</span>
<span class="font-body-sm text-body-sm text-primary">45%</span>
</div>
<div class="h-1.5 w-full bg-surface-container-high rounded-full overflow-hidden">
<div class="h-full bg-primary w-[45%] rounded-full shadow-[0_0_10px_rgba(118,219,143,0.5)]"></div>
</div>
</div>
</div>
<!-- Dataset List -->
<div class="glass-panel rounded-xl p-6 flex-1">
<div class="flex justify-between items-center mb-4">
<h2 class="font-headline-sm text-headline-sm text-on-surface">Active Datasets</h2>
<button class="text-primary hover:text-primary-fixed transition-colors">
<span class="material-symbols-outlined">filter_list</span>
</button>
</div>
<ul class="space-y-2">
<li class="glass-panel-hover p-3 rounded-lg border border-transparent cursor-pointer transition-all duration-200 flex items-center justify-between group bg-surface-container-high/30 border-l-2 border-l-primary">
<div class="flex items-center">
<span class="material-symbols-outlined text-primary mr-3 text-[20px]">database</span>
<div>
<div class="font-body-sm text-body-sm text-on-surface font-semibold">SUNAT Aduanas</div>
<div class="font-label-md text-label-md text-on-surface-variant mt-0.5">840K rows • Verified</div>
</div>
</div>
<span class="material-symbols-outlined text-on-surface-variant opacity-0 group-hover:opacity-100 transition-opacity">chevron_right</span>
</li>
<li class="glass-panel-hover p-3 rounded-lg border border-transparent cursor-pointer transition-all duration-200 flex items-center justify-between group">
<div class="flex items-center">
<span class="material-symbols-outlined text-on-surface-variant mr-3 text-[20px]">grass</span>
<div>
<div class="font-body-sm text-body-sm text-on-surface">MIDAGRI Prices</div>
<div class="font-label-md text-label-md text-on-surface-variant mt-0.5">120K rows • Pending</div>
</div>
</div>
<span class="material-symbols-outlined text-on-surface-variant opacity-0 group-hover:opacity-100 transition-opacity">chevron_right</span>
</li>
<li class="glass-panel-hover p-3 rounded-lg border border-transparent cursor-pointer transition-all duration-200 flex items-center justify-between group">
<div class="flex items-center">
<span class="material-symbols-outlined text-on-surface-variant mr-3 text-[20px]">partly_cloudy_day</span>
<div>
<div class="font-body-sm text-body-sm text-on-surface">SENAMHI Weather</div>
<div class="font-label-md text-label-md text-on-surface-variant mt-0.5">45K rows • Real-time</div>
</div>
</div>
<span class="material-symbols-outlined text-on-surface-variant opacity-0 group-hover:opacity-100 transition-opacity">chevron_right</span>
</li>
<li class="glass-panel-hover p-3 rounded-lg border border-transparent cursor-pointer transition-all duration-200 flex items-center justify-between group">
<div class="flex items-center">
<span class="material-symbols-outlined text-on-surface-variant mr-3 text-[20px]">travel_explore</span>
<div>
<div class="font-body-sm text-body-sm text-on-surface">TradeMap</div>
<div class="font-label-md text-label-md text-on-surface-variant mt-0.5">195K rows • Historical</div>
</div>
</div>
<span class="material-symbols-outlined text-on-surface-variant opacity-0 group-hover:opacity-100 transition-opacity">chevron_right</span>
</li>
</ul>
</div>
</div>
<!-- Right Column: Data Preview -->
<div class="lg:col-span-2 glass-panel rounded-xl p-6 flex flex-col h-[700px]">
<div class="flex justify-between items-center mb-6">
<div>
<h2 class="font-headline-sm text-headline-sm text-on-surface flex items-center">
<span class="material-symbols-outlined text-primary mr-2">view_list</span>
                                    Experimental Dataset Preview
                                </h2>
<p class="font-body-sm text-body-sm text-on-surface-variant mt-1">Showing first 20 rows of ingested telemetry</p>
</div>
<div class="flex space-x-2">
<button class="p-2 glass-panel-hover rounded text-on-surface-variant transition-colors" title="Export Segment">
<span class="material-symbols-outlined text-[20px]">download</span>
</button>
<button class="p-2 glass-panel-hover rounded text-on-surface-variant transition-colors" title="View Logs">
<span class="material-symbols-outlined text-[20px]">terminal</span>
</button>
</div>
</div>
<!-- Table Container -->
<div class="flex-1 overflow-auto border border-white/5 rounded-lg bg-surface-container-low/50 relative">
<table class="w-full text-left border-collapse whitespace-nowrap">
<thead class="sticky top-0 bg-surface-container-high/90 backdrop-blur-md z-10">
<tr>
<th class="font-label-md text-label-md text-on-surface-variant px-4 py-3 border-b-2 border-primary/50 uppercase tracking-wider">RUC</th>
<th class="font-label-md text-label-md text-on-surface-variant px-4 py-3 border-b-2 border-primary/50 uppercase tracking-wider">FOB (USD)</th>
<th class="font-label-md text-label-md text-on-surface-variant px-4 py-3 border-b-2 border-primary/50 uppercase tracking-wider">Volume (KG)</th>
<th class="font-label-md text-label-md text-on-surface-variant px-4 py-3 border-b-2 border-primary/50 uppercase tracking-wider">Date</th>
<th class="font-label-md text-label-md text-on-surface-variant px-4 py-3 border-b-2 border-primary/50 uppercase tracking-wider">Status</th>
</tr>
</thead>
<tbody class="font-mono-data text-mono-data text-on-surface" id="preview-table-body">
<!-- Rows generated via JS for compactness, simulating 20 rows -->
<script>
                                        const tbody = document.getElementById('preview-table-body');
                                        const statuses = ['VERIFIED', 'PENDING', 'FLAGGED'];
                                        const statusColors = {'VERIFIED': 'text-primary', 'PENDING': 'text-tertiary', 'FLAGGED': 'text-error animate-pulse'};
                                        
                                        for(let i=1; i<=20; i++) {
                                            const bgClass = i % 2 === 0 ? 'bg-white/[0.02]' : '';
                                            const status = statuses[Math.floor(Math.random() * 3)];
                                            const ruc = `20${Math.floor(100000000 + Math.random() * 900000000)}`;
                                            const fob = (Math.random() * 50000).toFixed(2);
                                            const vol = (Math.random() * 10000).toFixed(2);
                                            
                                            // Mock dates within last 30 days
                                            const d = new Date();
                                            d.setDate(d.getDate() - Math.floor(Math.random() * 30));
                                            const dateStr = d.toISOString().split('T')[0];

                                            tbody.innerHTML += `
                                                <tr class="border-b border-white/5 hover:bg-white/5 transition-colors ${bgClass}">
                                                    <td class="px-4 py-2.5">${ruc}</td>
                                                    <td class="px-4 py-2.5">$${fob}</td>
                                                    <td class="px-4 py-2.5">${vol}</td>
                                                    <td class="px-4 py-2.5 text-on-surface-variant">${dateStr}</td>
                                                    <td class="px-4 py-2.5 ${statusColors[status]} font-bold text-[12px]">${status}</td>
                                                </tr>
                                            `;
                                        }
                                    </script>
</tbody>
</table>
</div>
</div>
</div>
</div>
</div>
</main>
<script>
        // Simple Drag and Drop interaction script
        const dropzone = document.getElementById('dropzone');
        
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropzone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults (e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropzone.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropzone.addEventListener(eventName, unhighlight, false);
        });

        function highlight(e) {
            dropzone.classList.add('drag-active');
        }

        function unhighlight(e) {
            dropzone.classList.remove('drag-active');
        }
    </script>
</body></html>

<!-- Auditor Login -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Login - AgroAudit Precision</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Outfit:wght@600;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            "colors": {
                    "on-error": "#690005",
                    "on-tertiary-container": "#002d43",
                    "inverse-primary": "#006d33",
                    "background": "#0f150f",
                    "secondary-fixed-dim": "#9dd3a7",
                    "secondary-container": "#205331",
                    "surface-container-low": "#171d17",
                    "primary": "#76db8f",
                    "surface-tint": "#76db8f",
                    "on-tertiary-fixed-variant": "#004c6e",
                    "surface-variant": "#30362f",
                    "surface-dim": "#0f150f",
                    "primary-container": "#3da35d",
                    "on-primary-fixed-variant": "#005225",
                    "error-container": "#93000a",
                    "outline": "#889487",
                    "on-tertiary-fixed": "#001e2f",
                    "surface-bright": "#343b34",
                    "secondary": "#9dd3a7",
                    "on-tertiary": "#00344d",
                    "surface-container": "#1b211b",
                    "primary-fixed": "#92f8a9",
                    "secondary-fixed": "#b8f0c2",
                    "surface-container-highest": "#30362f",
                    "error": "#ffb4ab",
                    "primary-fixed-dim": "#76db8f",
                    "on-secondary-fixed": "#00210c",
                    "on-primary": "#003918",
                    "tertiary-fixed": "#c9e6ff",
                    "surface": "#0f150f",
                    "on-primary-fixed": "#00210b",
                    "outline-variant": "#3f4a3f",
                    "surface-container-lowest": "#0a100a",
                    "tertiary": "#89ceff",
                    "on-primary-container": "#003114",
                    "on-secondary-container": "#8fc599",
                    "tertiary-fixed-dim": "#89ceff",
                    "on-error-container": "#ffdad6",
                    "on-secondary": "#01391a",
                    "inverse-on-surface": "#2c322b",
                    "tertiary-container": "#009ada",
                    "on-surface": "#dee4da",
                    "surface-container-high": "#252c25",
                    "on-surface-variant": "#becabc",
                    "on-secondary-fixed-variant": "#1e502e",
                    "on-background": "#dee4da",
                    "inverse-surface": "#dee4da"
            },
            "borderRadius": {
                    "DEFAULT": "0.125rem",
                    "lg": "0.25rem",
                    "xl": "0.5rem",
                    "full": "0.75rem"
            },
            "spacing": {
                    "card-gap": "20px",
                    "gutter": "16px",
                    "container-padding": "24px",
                    "unit": "4px"
            },
            "fontFamily": {
                    "mono-data": [
                            "monospace"
                    ],
                    "body-lg": [
                            "Inter"
                    ],
                    "headline-lg": [
                            "Outfit"
                    ],
                    "body-md": [
                            "Inter"
                    ],
                    "label-md": [
                            "Inter"
                    ],
                    "display-lg": [
                            "Outfit"
                    ],
                    "body-sm": [
                            "Inter"
                    ],
                    "headline-sm": [
                            "Outfit"
                    ],
                    "headline-md": [
                            "Outfit"
                    ]
            },
            "fontSize": {
                    "mono-data": [
                            "14px",
                            {
                                    "lineHeight": "20px",
                                    "fontWeight": "500"
                            }
                    ],
                    "body-lg": [
                            "18px",
                            {
                                    "lineHeight": "28px",
                                    "fontWeight": "400"
                            }
                    ],
                    "headline-lg": [
                            "32px",
                            {
                                    "lineHeight": "40px",
                                    "fontWeight": "600"
                            }
                    ],
                    "body-md": [
                            "16px",
                            {
                                    "lineHeight": "24px",
                                    "fontWeight": "400"
                            }
                    ],
                    "label-md": [
                            "12px",
                            {
                                    "lineHeight": "16px",
                                    "letterSpacing": "0.05em",
                                    "fontWeight": "600"
                            }
                    ],
                    "display-lg": [
                            "48px",
                            {
                                    "lineHeight": "56px",
                                    "letterSpacing": "-0.02em",
                                    "fontWeight": "700"
                            }
                    ],
                    "body-sm": [
                            "14px",
                            {
                                    "lineHeight": "20px",
                                    "fontWeight": "400"
                            }
                    ],
                    "headline-sm": [
                            "20px",
                            {
                                    "lineHeight": "28px",
                                    "fontWeight": "600"
                            }
                    ],
                    "headline-md": [
                            "24px",
                            {
                                    "lineHeight": "32px",
                                    "fontWeight": "600"
                            }
                    ]
            }
          }
        }
      }
    </script>
<style>
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .input-glass {
            background: transparent;
            border: 1px solid rgba(136, 148, 135, 0.5); /* outline color with opacity */
            transition: all 0.3s ease;
        }
        .input-glass:focus {
            background: rgba(255, 255, 255, 0.05);
            border-color: #76db8f; /* primary color */
            box-shadow: 0 0 15px rgba(118, 219, 143, 0.2);
            outline: none;
        }
        .btn-glow:hover {
            box-shadow: 0 0 20px rgba(61, 163, 93, 0.4);
        }
        .grid-bg {
            background-image: 
                linear-gradient(to right, rgba(255,255,255,0.02) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(255,255,255,0.02) 1px, transparent 1px);
            background-size: 40px 40px;
        }
    </style>
</head>
<body class="bg-background text-on-background min-h-screen flex items-center justify-center relative overflow-hidden font-body-md">
<!-- Background Texture -->
<div class="absolute inset-0 z-0">
<div class="absolute inset-0 bg-gradient-to-br from-surface-container-lowest via-background to-surface-container-highest"></div>
<div class="absolute inset-0 grid-bg"></div>
<div class="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-container rounded-full mix-blend-screen filter blur-[120px] opacity-20 animate-pulse"></div>
<div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-tertiary-container rounded-full mix-blend-screen filter blur-[120px] opacity-10"></div>
</div>
<!-- Login Container -->
<main class="w-full max-w-md px-container-padding relative z-10">
<!-- Logo Area -->
<div class="text-center mb-8">
<h1 class="font-display-lg text-display-lg text-primary flex items-center justify-center gap-2 mb-2">
<span class="material-symbols-outlined" style="font-size: 48px; font-variation-settings: 'FILL' 1;">eco</span>
</h1>
<h2 class="font-headline-md text-headline-md text-on-surface tracking-tight">AgroAudit Precision</h2>
<p class="font-body-sm text-body-sm text-on-surface-variant mt-2">Vigilance Level: High • Secure Terminal</p>
</div>
<!-- Glassmorphism Card -->
<div class="glass-card rounded-xl p-8 relative overflow-hidden">
<!-- Subtle top border highlight -->
<div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-primary to-transparent opacity-50"></div>
<form class="space-y-6" id="loginForm">
<!-- Header -->
<div>
<h3 class="font-headline-sm text-headline-sm text-on-surface">Operator Authentication</h3>
<p class="font-body-sm text-body-sm text-on-surface-variant mt-1">Enter your credentials to access the telemetry oversight system.</p>
</div>
<!-- Username/Email Field -->
<div class="space-y-2 relative group">
<label class="font-label-md text-label-md text-on-surface-variant block" for="identifier">Auditor ID / Email</label>
<div class="relative">
<span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-outline group-focus-within:text-primary transition-colors">person</span>
<input class="input-glass w-full rounded-lg py-3 pl-10 pr-4 font-body-md text-body-md text-on-surface placeholder:text-outline-variant" id="identifier" name="identifier" placeholder="e.g. AUD-7492 or email" required="" type="text"/>
</div>
</div>
<!-- Password Field -->
<div class="space-y-2 relative group">
<label class="font-label-md text-label-md text-on-surface-variant block flex justify-between" for="password">
<span>Access Code</span>
<a class="text-primary hover:text-primary-fixed transition-colors" href="#">Forgot Code?</a>
</label>
<div class="relative">
<span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-outline group-focus-within:text-primary transition-colors">lock</span>
<input class="input-glass w-full rounded-lg py-3 pl-10 pr-12 font-body-md text-body-md text-on-surface placeholder:text-outline-variant" id="password" name="password" placeholder="Enter 256-bit encryption key" required="" type="password"/>
<button class="absolute right-3 top-1/2 -translate-y-1/2 text-outline hover:text-on-surface transition-colors focus:outline-none" id="togglePassword" type="button">
<span class="material-symbols-outlined" id="visibilityIcon">visibility</span>
</button>
</div>
<!-- Error State Message (Hidden by default) -->
<p class="hidden font-body-sm text-body-sm text-error mt-2 flex items-center gap-1" id="errorMessage">
<span class="material-symbols-outlined" style="font-size: 16px;">error</span>
                        Invalid credentials. Telemetry access denied.
                    </p>
</div>
<!-- Action Button -->
<button class="w-full bg-primary-container text-on-primary-container font-headline-sm text-headline-sm rounded-lg py-3 px-6 mt-8 flex items-center justify-center gap-2 btn-glow transition-all duration-200 transform active:scale-95" type="submit">
<span>Initialize Session</span>
<span class="material-symbols-outlined">login</span>
</button>
<!-- System Status -->
<div class="flex items-center justify-center gap-2 mt-6 pt-6 border-t border-white/10">
<span class="w-2 h-2 rounded-full bg-primary animate-pulse shadow-[0_0_8px_#76db8f]"></span>
<span class="font-mono-data text-mono-data text-on-surface-variant tracking-wider">SYSTEM SECURE</span>
</div>
</form>
</div>
</main>
<script>
        // Password Visibility Toggle
        const togglePassword = document.getElementById('togglePassword');
        const passwordInput = document.getElementById('password');
        const visibilityIcon = document.getElementById('visibilityIcon');

        togglePassword.addEventListener('click', () => {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            visibilityIcon.textContent = type === 'password' ? 'visibility' : 'visibility_off';
        });

        // Form Submission Simulation for Error State
        const loginForm = document.getElementById('loginForm');
        const errorMessage = document.getElementById('errorMessage');
        const passwordContainer = document.getElementById('password').parentElement;

        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            // Simulate an error for demonstration purposes
            const passwordVal = passwordInput.value;
            if(passwordVal !== 'correct') { // Simple logic for demo
                errorMessage.classList.remove('hidden');
                passwordInput.classList.remove('border-[rgba(136,148,135,0.5)]', 'focus:border-[#76db8f]', 'focus:shadow-[0_0_15px_rgba(118,219,143,0.2)]');
                passwordInput.classList.add('border-error', 'focus:border-error', 'focus:shadow-[0_0_15px_rgba(255,180,171,0.2)]');
                
                // Shake effect
                loginForm.classList.add('animate-[shake_0.5s_ease-in-out]');
                setTimeout(() => {
                    loginForm.classList.remove('animate-[shake_0.5s_ease-in-out]');
                }, 500);

            } else {
                 errorMessage.classList.add('hidden');
                 // Reset classes if needed
            }
        });

        // Custom Shake Animation injected via style
        const style = document.createElement('style');
        style.innerHTML = `
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
                20%, 40%, 60%, 80% { transform: translateX(5px); }
            }
        `;
        document.head.appendChild(style);
    </script>
</body></html>

<!-- Operation Detail (AI Explicable) -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Integrated Operation Detail - AgroAudit Precision</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Outfit:wght@600;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    "colors": {
                        "on-error": "#690005",
                        "on-tertiary-container": "#002d43",
                        "inverse-primary": "#006d33",
                        "background": "#0f150f",
                        "secondary-fixed-dim": "#9dd3a7",
                        "secondary-container": "#205331",
                        "surface-container-low": "#171d17",
                        "primary": "#76db8f",
                        "surface-tint": "#76db8f",
                        "on-tertiary-fixed-variant": "#004c6e",
                        "surface-variant": "#30362f",
                        "surface-dim": "#0f150f",
                        "primary-container": "#3da35d",
                        "on-primary-fixed-variant": "#005225",
                        "error-container": "#93000a",
                        "outline": "#889487",
                        "on-tertiary-fixed": "#001e2f",
                        "surface-bright": "#343b34",
                        "secondary": "#9dd3a7",
                        "on-tertiary": "#00344d",
                        "surface-container": "#1b211b",
                        "primary-fixed": "#92f8a9",
                        "secondary-fixed": "#b8f0c2",
                        "surface-container-highest": "#30362f",
                        "error": "#ffb4ab",
                        "primary-fixed-dim": "#76db8f",
                        "on-secondary-fixed": "#00210c",
                        "on-primary": "#003918",
                        "tertiary-fixed": "#c9e6ff",
                        "surface": "#0f150f",
                        "on-primary-fixed": "#00210b",
                        "outline-variant": "#3f4a3f",
                        "surface-container-lowest": "#0a100a",
                        "tertiary": "#89ceff",
                        "on-primary-container": "#003114",
                        "on-secondary-container": "#8fc599",
                        "tertiary-fixed-dim": "#89ceff",
                        "on-error-container": "#ffdad6",
                        "on-secondary": "#01391a",
                        "inverse-on-surface": "#2c322b",
                        "tertiary-container": "#009ada",
                        "on-surface": "#dee4da",
                        "surface-container-high": "#252c25",
                        "on-surface-variant": "#becabc",
                        "on-secondary-fixed-variant": "#1e502e",
                        "on-background": "#dee4da",
                        "inverse-surface": "#dee4da"
                    },
                    "borderRadius": {
                        "DEFAULT": "0.125rem",
                        "lg": "0.25rem",
                        "xl": "0.5rem",
                        "full": "0.75rem"
                    },
                    "spacing": {
                        "card-gap": "20px",
                        "gutter": "16px",
                        "container-padding": "24px",
                        "unit": "4px"
                    },
                    "fontFamily": {
                        "mono-data": ["monospace"],
                        "body-lg": ["Inter"],
                        "headline-lg": ["Outfit"],
                        "body-md": ["Inter"],
                        "label-md": ["Inter"],
                        "display-lg": ["Outfit"],
                        "body-sm": ["Inter"],
                        "headline-sm": ["Outfit"],
                        "headline-md": ["Outfit"]
                    },
                    "fontSize": {
                        "mono-data": ["14px", { "lineHeight": "20px", "fontWeight": "500" }],
                        "body-lg": ["18px", { "lineHeight": "28px", "fontWeight": "400" }],
                        "headline-lg": ["32px", { "lineHeight": "40px", "fontWeight": "600" }],
                        "body-md": ["16px", { "lineHeight": "24px", "fontWeight": "400" }],
                        "label-md": ["12px", { "lineHeight": "16px", "letterSpacing": "0.05em", "fontWeight": "600" }],
                        "display-lg": ["48px", { "lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "700" }],
                        "body-sm": ["14px", { "lineHeight": "20px", "fontWeight": "400" }],
                        "headline-sm": ["20px", { "lineHeight": "28px", "fontWeight": "600" }],
                        "headline-md": ["24px", { "lineHeight": "32px", "fontWeight": "600" }]
                    }
                }
            }
        }
    </script>
<style>
        /* Glassmorphism Utilities */
        .glass-panel {
            background-color: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .glass-panel-elevated {
            background-color: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(40px);
            -webkit-backdrop-filter: blur(40px);
            border: 1px solid rgba(61, 163, 93, 0.3); /* Emerald tint */
            box-shadow: 0 0 30px rgba(61, 163, 93, 0.15);
        }
        /* Custom Scrollbar for data density */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.4);
        }
    </style>
</head>
<body class="bg-background text-on-surface font-body-md antialiased overflow-hidden flex h-screen w-full">
<!-- Desktop SideNavBar (Hidden on Mobile) -->
<nav class="hidden md:flex flex-col h-screen w-64 fixed left-0 top-0 py-6 bg-surface/5 dark:bg-surface/5 backdrop-blur-xl border-r border-white/10 z-40">
<div class="px-6 mb-8">
<h1 class="font-headline-sm text-headline-sm text-primary tracking-tight">AgroAudit Precision</h1>
</div>
<div class="px-4 mb-6 flex items-center gap-3 bg-white/5 mx-4 p-3 rounded-lg border border-white/10">
<div class="w-10 h-10 rounded-full bg-surface-container overflow-hidden border border-outline/30 flex-shrink-0">
<img alt="System Operator" class="w-full h-full object-cover" data-alt="A clinical, high-contrast headshot of a system auditor wearing a dark tactical headset, set against a dark green glowing telemetry background. Lighting is sharp and moody." src="https://lh3.googleusercontent.com/aida-public/AB6AXuC4EsDvKgnnCJ8HhamvgrzYtcrUMPcpiaTy_MYU9GzHn1rj67k6VmX71_0v5kOUMFwCWT8RgooIiRw8bjN6GdM0TzyCxYgIGqBFo1yJR5y8WsC0XEDZk7Y1nurD4V0XmvJkg8Gv9Zon_X8I_dVRQh1QZ3cXKP5BGnPr8AvbeLPArvSFKKIpw6CmimO2RArpOxQd8mzgUAkjDszF3ihdhzQO7_Ejp5yky72ctlfyg2s7ktzti7rYrLJB1uYqI70mC8EYNaKj-rCKtvE"/>
</div>
<div>
<div class="font-label-md text-label-md text-on-surface">Auditor Terminal</div>
<div class="font-mono-data text-[10px] text-error flex items-center gap-1">
<span class="w-2 h-2 rounded-full bg-error animate-pulse"></span>
                    Vigilance: High
                </div>
</div>
</div>
<div class="flex-1 px-4 flex flex-col gap-1 overflow-y-auto">
<a class="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:bg-white/10 transition-all translate-x-1 duration-200" href="#">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 0;">dashboard</span>
<span class="font-label-md text-label-md">Dashboard</span>
</a>
<!-- Active State -->
<a class="flex items-center gap-3 px-4 py-3 rounded-lg text-primary font-bold border-l-4 border-primary bg-white/5 hover:bg-white/10 transition-all translate-x-1 duration-200" href="#">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">warning</span>
<span class="font-label-md text-label-md">Alerts</span>
</a>
<a class="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:bg-white/10 transition-all translate-x-1 duration-200" href="#">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 0;">troubleshoot</span>
<span class="font-label-md text-label-md">Data Explorer</span>
</a>
<a class="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:bg-white/10 transition-all translate-x-1 duration-200" href="#">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 0;">settings</span>
<span class="font-label-md text-label-md">Configuration</span>
</a>
<a class="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:bg-white/10 transition-all translate-x-1 duration-200" href="#">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 0;">sensors</span>
<span class="font-label-md text-label-md">Telemetry</span>
</a>
</div>
<div class="px-4 mt-auto pt-4 border-t border-white/10 flex flex-col gap-2">
<button class="w-full bg-primary/10 border border-primary text-primary hover:bg-primary/20 transition-colors py-2 rounded-lg font-label-md text-label-md flex justify-center items-center gap-2">
<span class="material-symbols-outlined text-[18px]">add</span>
                New Inspection
            </button>
<div class="flex justify-between mt-4">
<button class="text-on-surface-variant hover:text-on-surface p-2 rounded-lg hover:bg-white/5 transition-colors">
<span class="material-symbols-outlined">support_agent</span>
</button>
<button class="text-on-surface-variant hover:text-on-surface p-2 rounded-lg hover:bg-white/5 transition-colors">
<span class="material-symbols-outlined">logout</span>
</button>
</div>
</div>
</nav>
<!-- Main Content Area -->
<main class="flex-1 flex flex-col md:ml-64 w-full h-full relative">
<!-- TopNavBar -->
<header class="flex justify-between items-center px-container-padding w-full h-16 sticky top-0 z-30 bg-surface/5 dark:bg-surface/5 backdrop-blur-md shadow-sm">
<div class="flex items-center gap-4">
<!-- Mobile Menu Trigger (Hidden on Desktop) -->
<button class="md:hidden text-on-surface">
<span class="material-symbols-outlined">menu</span>
</button>
<div class="md:hidden font-headline-sm text-headline-sm font-bold text-primary">AgroAudit</div>
<div class="hidden md:flex items-center bg-surface-container-high rounded-full px-4 py-1.5 border border-white/5 focus-within:border-primary/50 transition-colors">
<span class="material-symbols-outlined text-on-surface-variant mr-2 text-[20px]">search</span>
<input class="bg-transparent border-none focus:ring-0 text-body-sm font-body-sm text-on-surface placeholder:text-on-surface-variant/50 w-64 p-0" placeholder="Search DAM, RUC..." type="text"/>
</div>
</div>
<div class="flex items-center gap-2">
<button class="p-2 rounded-full text-on-surface-variant hover:bg-white/5 transition-colors hover:text-primary relative scale-95 duration-150">
<span class="material-symbols-outlined">notifications</span>
<span class="absolute top-2 right-2 w-2 h-2 bg-error rounded-full"></span>
</button>
<button class="p-2 rounded-full text-on-surface-variant hover:bg-white/5 transition-colors scale-95 duration-150">
<span class="material-symbols-outlined">help_outline</span>
</button>
</div>
</header>
<!-- Canvas / Dashboard Content -->
<div class="flex-1 overflow-y-auto p-container-padding pb-24 md:pb-container-padding">
<!-- Operation Header -->
<div class="mb-gutter">
<div class="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-4">
<div>
<div class="flex items-center gap-3 mb-1">
<span class="bg-error/20 text-error border border-error/30 px-2 py-0.5 rounded text-[10px] font-mono-data tracking-wider uppercase">Condition A</span>
<span class="text-on-surface-variant font-mono-data text-[12px]">Recorded: Just Now</span>
</div>
<h2 class="font-headline-lg text-headline-lg text-on-surface flex items-center gap-3">
<span class="material-symbols-outlined text-primary text-[32px]">inventory_2</span>
                            DAM #012345
                        </h2>
</div>
<div class="flex gap-3">
<button class="glass-panel px-4 py-2 rounded-lg font-label-md text-label-md text-on-surface hover:bg-white/10 transition-colors flex items-center gap-2">
<span class="material-symbols-outlined text-[18px]">history</span>
                            History
                        </button>
<button class="glass-panel px-4 py-2 rounded-lg font-label-md text-label-md text-on-surface hover:bg-white/10 transition-colors flex items-center gap-2">
<span class="material-symbols-outlined text-[18px]">download</span>
                            Export
                        </button>
</div>
</div>
<!-- Meta Badges -->
<div class="flex flex-wrap gap-2">
<div class="glass-panel px-3 py-1.5 rounded-md flex items-center gap-2 border-l-2 border-l-primary/50">
<span class="material-symbols-outlined text-[16px] text-on-surface-variant">corporate_fare</span>
<span class="font-mono-data text-mono-data text-on-surface-variant">RUC:</span>
<span class="font-mono-data text-mono-data text-on-surface">20123456789</span>
</div>
<div class="glass-panel px-3 py-1.5 rounded-md flex items-center gap-2 border-l-2 border-l-primary/50">
<span class="material-symbols-outlined text-[16px] text-on-surface-variant">storefront</span>
<span class="font-body-sm text-body-sm text-on-surface-variant">Company:</span>
<span class="font-body-sm text-body-sm text-on-surface font-medium">Agroworld S.A.C.</span>
</div>
<div class="glass-panel px-3 py-1.5 rounded-md flex items-center gap-2 border-l-2 border-l-secondary/50">
<span class="material-symbols-outlined text-[16px] text-on-surface-variant">eco</span>
<span class="font-body-sm text-body-sm text-on-surface-variant">Product:</span>
<span class="font-body-sm text-body-sm text-on-surface font-medium">Palta Hass</span>
</div>
<div class="glass-panel px-3 py-1.5 rounded-md flex items-center gap-2 border-l-2 border-l-tertiary/50">
<span class="material-symbols-outlined text-[16px] text-on-surface-variant">sailing</span>
<span class="font-body-sm text-body-sm text-on-surface-variant">Destination:</span>
<span class="font-body-sm text-body-sm text-on-surface font-medium">Rotterdam</span>
</div>
</div>
</div>
<!-- Grid Layout -->
<div class="grid grid-cols-1 xl:grid-cols-12 gap-card-gap">
<!-- Layer 1: GBDT Prediction (Col 1-6) -->
<div class="xl:col-span-6 glass-panel rounded-xl p-6 relative overflow-hidden group">
<!-- Subtle background gradient -->
<div class="absolute inset-0 bg-gradient-to-br from-error/5 to-transparent opacity-50 pointer-events-none"></div>
<h3 class="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2 mb-6">
<span class="material-symbols-outlined text-secondary">monitoring</span>
                        Layer 1: Value Prediction (GBDT)
                    </h3>
<div class="flex flex-col md:flex-row items-center gap-8">
<!-- Simulated Gauge / Comparison -->
<div class="flex-1 w-full space-y-6">
<div>
<div class="flex justify-between font-label-md text-label-md mb-2">
<span class="text-on-surface-variant">Declared FOB</span>
<span class="text-on-surface font-mono-data">$120,000</span>
</div>
<div class="h-3 w-full bg-surface-container rounded-full overflow-hidden">
<div class="h-full bg-surface-variant w-[70%] rounded-full relative"></div>
</div>
</div>
<div>
<div class="flex justify-between font-label-md text-label-md mb-2">
<span class="text-primary flex items-center gap-1">
<span class="material-symbols-outlined text-[14px]">psychiatry</span> Expected FOB (Model)
                                    </span>
<span class="text-primary font-mono-data">$135,000</span>
</div>
<div class="h-3 w-full bg-surface-container rounded-full overflow-hidden">
<div class="h-full bg-primary/80 w-[82.5%] rounded-full relative shadow-[0_0_10px_rgba(118,219,143,0.5)]">
<!-- Marker for declared value -->
<div class="absolute top-0 bottom-0 left-[84.8%] w-1 bg-white/50 z-10"></div>
</div>
</div>
</div>
</div>
<!-- Deviation Highlight -->
<div class="w-32 h-32 rounded-full border-4 border-error/20 flex flex-col items-center justify-center relative shrink-0">
<!-- SVG for circular progress indication -->
<svg class="absolute inset-0 w-full h-full -rotate-90" viewbox="0 0 100 100">
<circle class="text-error/20" cx="50" cy="50" fill="none" r="46" stroke="currentColor" stroke-width="4"></circle>
<circle class="text-error drop-shadow-[0_0_8px_rgba(255,180,171,0.6)]" cx="50" cy="50" fill="none" r="46" stroke="currentColor" stroke-dasharray="289" stroke-dashoffset="250" stroke-width="4"></circle>
</svg>
<span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-widest text-[10px]">Deviation</span>
<span class="font-display-lg text-[32px] text-error font-bold leading-none mt-1">12.5%</span>
</div>
</div>
</div>
<!-- Layer 2: Ensemble Score (Col 7-12) -->
<div class="xl:col-span-6 glass-panel rounded-xl p-6 relative border-error/30">
<div class="absolute top-0 left-0 w-full h-1 bg-error animate-pulse"></div>
<h3 class="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2 mb-2">
<span class="material-symbols-outlined text-error">gavel</span>
                        Layer 2: Anomaly Severity
                    </h3>
<p class="font-body-sm text-body-sm text-on-surface-variant mb-6">Consensus scoring across Isolation Forest, Local Outlier Factor, and ECOD algorithms.</p>
<div class="flex items-center justify-center h-40 glass-panel-elevated bg-error/5 border-error/20 rounded-lg relative overflow-hidden group">
<!-- Pulsing background effect -->
<div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-error/10 via-transparent to-transparent animate-pulse opacity-50"></div>
<div class="flex flex-col items-center z-10">
<span class="material-symbols-outlined text-[48px] text-error mb-2 drop-shadow-[0_0_15px_rgba(255,180,171,0.5)]">warning_amber</span>
<h4 class="font-display-lg text-[36px] text-error tracking-tight drop-shadow-[0_0_10px_rgba(255,180,171,0.3)]">HIGH RISK</h4>
<div class="font-mono-data text-[12px] text-error/80 mt-2 bg-error/10 px-3 py-1 rounded-full border border-error/20">
                                Confidence Score: 0.94
                            </div>
</div>
</div>
</div>
<!-- Layer 3: SHAP Explicability (Full Width) -->
<div class="xl:col-span-12 glass-panel rounded-xl p-6">
<div class="flex justify-between items-end mb-6">
<div>
<h3 class="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2">
<span class="material-symbols-outlined text-tertiary">analytics</span>
                                Layer 3: Influence Variables (SHAP)
                            </h3>
<p class="font-body-sm text-body-sm text-on-surface-variant mt-1">Factors driving the anomaly score (Red increases risk, Blue decreases risk).</p>
</div>
<button class="text-primary text-label-md font-label-md flex items-center hover:underline">
                            View Model Details <span class="material-symbols-outlined text-[16px] ml-1">arrow_forward</span>
</button>
</div>
<div class="grid grid-cols-1 lg:grid-cols-2 gap-x-12 gap-y-4">
<!-- Variable 1 -->
<div class="flex items-center gap-4 group">
<div class="w-1/3 text-right font-label-md text-label-md text-on-surface truncate group-hover:text-primary transition-colors">Residual Price</div>
<div class="w-2/3 flex items-center gap-2">
<div class="h-4 bg-error/80 rounded-r-sm" style="width: 85%;"></div>
<span class="font-mono-data text-[12px] text-error">+0.32</span>
</div>
</div>
<!-- Variable 2 -->
<div class="flex items-center gap-4 group">
<div class="w-1/3 text-right font-label-md text-label-md text-on-surface truncate group-hover:text-primary transition-colors">Temp. Deviation</div>
<div class="w-2/3 flex items-center gap-2">
<div class="h-4 bg-error/80 rounded-r-sm" style="width: 60%;"></div>
<span class="font-mono-data text-[12px] text-error">+0.21</span>
</div>
</div>
<!-- Variable 3 -->
<div class="flex items-center gap-4 group">
<div class="w-1/3 text-right font-label-md text-label-md text-on-surface truncate group-hover:text-primary transition-colors">History Profile</div>
<div class="w-2/3 flex items-center gap-2 flex-row-reverse justify-end">
<div class="h-4 bg-tertiary/80 rounded-l-sm" style="width: 45%;"></div>
<span class="font-mono-data text-[12px] text-tertiary">-0.15</span>
</div>
</div>
<!-- Variable 4 -->
<div class="flex items-center gap-4 group">
<div class="w-1/3 text-right font-label-md text-label-md text-on-surface truncate group-hover:text-primary transition-colors">Rainfall (Origin)</div>
<div class="w-2/3 flex items-center gap-2">
<div class="h-4 bg-error/60 rounded-r-sm" style="width: 35%;"></div>
<span class="font-mono-data text-[12px] text-error">+0.12</span>
</div>
</div>
<!-- Variable 5 -->
<div class="flex items-center gap-4 group">
<div class="w-1/3 text-right font-label-md text-label-md text-on-surface truncate group-hover:text-primary transition-colors">Logistics Delay</div>
<div class="w-2/3 flex items-center gap-2">
<div class="h-4 bg-error/50 rounded-r-sm" style="width: 20%;"></div>
<span class="font-mono-data text-[12px] text-error">+0.08</span>
</div>
</div>
</div>
</div>
<!-- Layer 4: RAG Report (Col 1-7) -->
<div class="xl:col-span-7 glass-panel rounded-xl p-6 flex flex-col">
<h3 class="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2 mb-4">
<span class="material-symbols-outlined text-primary">description</span>
                        Layer 4: AI Technical Narrative
                    </h3>
<div class="flex-1 glass-panel bg-surface-container-low/50 rounded-lg p-5 border border-white/5 font-body-md text-body-md text-on-surface-variant leading-relaxed overflow-y-auto">
<p class="mb-4">
                            The ensemble model flagged this operation due to a significant divergence between the declared FOB value and historical baselines for <span class="text-on-surface font-medium">Palta Hass</span> exported to <span class="text-on-surface font-medium">Rotterdam</span> during this seasonal window. 
                        </p>
<p class="mb-4">
                            The primary driver is the <strong class="text-error font-medium">Residual Price anomaly</strong>. Additionally, telemetry records indicate a localized <strong class="text-error font-medium">Temperature Deviation</strong> during transit to the port facility, which may correlate with quality degradation not reflected in the premium pricing claimed.
                        </p>
<p>
                            According to the <a class="text-primary hover:text-primary-fixed underline decoration-primary/30 underline-offset-2 transition-colors" href="#">Customs Directives regarding Perishables Valuation (Art 42.1)</a>, operations exhibiting &gt;10% negative deviation combined with logistical irregularities require manual verification of commercial invoices and phytosanitary certificates as outlined in <a class="text-primary hover:text-primary-fixed underline decoration-primary/30 underline-offset-2 transition-colors" href="#">FDA Phytosanitary Regs Annex B</a>.
                        </p>
</div>
<div class="mt-3 flex justify-end gap-2 text-on-surface-variant font-label-md text-[10px] uppercase tracking-wider">
<span class="flex items-center gap-1"><span class="material-symbols-outlined text-[14px]">auto_awesome</span> Generated by RAG Core v2.4</span>
</div>
</div>
<!-- Decision Panel (Col 8-12) -->
<div class="xl:col-span-5 glass-panel-elevated rounded-xl p-6 flex flex-col border-primary/20">
<h3 class="font-headline-sm text-headline-sm text-primary flex items-center gap-2 mb-6">
<span class="material-symbols-outlined">rule</span>
                        Operation Adjudication
                    </h3>
<form class="flex-1 flex flex-col space-y-6">
<!-- Radio Buttons -->
<div class="space-y-3">
<label class="flex items-center gap-3 p-3 rounded-lg border border-outline/30 cursor-pointer hover:bg-white/5 transition-colors focus-within:border-primary focus-within:bg-primary/5">
<input class="w-4 h-4 text-primary bg-transparent border-outline focus:ring-primary focus:ring-offset-background" name="adjudication" type="radio" value="confirmed"/>
<span class="font-body-md text-on-surface">Confirmed Anomaly</span>
</label>
<label class="flex items-center gap-3 p-3 rounded-lg border border-outline/30 cursor-pointer hover:bg-white/5 transition-colors focus-within:border-secondary focus-within:bg-secondary/5">
<input class="w-4 h-4 text-secondary bg-transparent border-outline focus:ring-secondary focus:ring-offset-background" name="adjudication" type="radio" value="false_alarm"/>
<span class="font-body-md text-on-surface">False Alarm (Model Drift)</span>
</label>
<label class="flex items-center gap-3 p-3 rounded-lg border border-outline/30 cursor-pointer hover:bg-white/5 transition-colors focus-within:border-tertiary focus-within:bg-tertiary/5">
<input class="w-4 h-4 text-tertiary bg-transparent border-outline focus:ring-tertiary focus:ring-offset-background" name="adjudication" type="radio" value="investigation"/>
<span class="font-body-md text-on-surface">Requires Physical Inspection</span>
</label>
</div>
<!-- Justification -->
<div class="space-y-2">
<label class="font-label-md text-label-md text-on-surface-variant flex justify-between">
                                Justification Note
                                <span class="font-mono-data text-[10px]">0 / 250</span>
</label>
<textarea class="w-full bg-transparent border border-outline/50 rounded-lg p-3 text-body-sm font-body-sm text-on-surface placeholder:text-on-surface-variant/40 focus:border-primary focus:ring-1 focus:ring-primary focus:bg-white/5 transition-all resize-none" placeholder="Enter technical rationale..." rows="3"></textarea>
</div>
<!-- Likert Scale -->
<div class="space-y-2">
<label class="font-label-md text-label-md text-on-surface-variant block">AI Comprehension Rating</label>
<div class="flex items-center gap-2">
<!-- Simulated 5-star rating -->
<button class="text-on-surface-variant hover:text-primary transition-colors" type="button"><span class="material-symbols-outlined text-[24px]">star</span></button>
<button class="text-on-surface-variant hover:text-primary transition-colors" type="button"><span class="material-symbols-outlined text-[24px]">star</span></button>
<button class="text-on-surface-variant hover:text-primary transition-colors" type="button"><span class="material-symbols-outlined text-[24px]">star</span></button>
<button class="text-on-surface-variant hover:text-primary transition-colors" type="button"><span class="material-symbols-outlined text-[24px]">star</span></button>
<button class="text-on-surface-variant hover:text-primary transition-colors" type="button"><span class="material-symbols-outlined text-[24px]">star</span></button>
</div>
</div>
<!-- Submit Action -->
<button class="w-full mt-auto bg-primary text-on-primary font-label-md text-label-md py-3 px-4 rounded-lg hover:bg-primary-fixed transition-colors flex justify-center items-center gap-2 shadow-[0_0_15px_rgba(118,219,143,0.3)] hover:shadow-[0_0_25px_rgba(118,219,143,0.5)]" type="submit">
<span class="material-symbols-outlined text-[18px]">send</span>
                            Submit Decision to Telemetry
                        </button>
</form>
</div>
</div>
</div>
</main>
<!-- Mobile Bottom NavBar -->
<nav class="md:hidden fixed bottom-0 left-0 w-full h-16 bg-surface/10 backdrop-blur-xl border-t border-white/5 z-50 flex justify-around items-center px-2">
<a class="flex flex-col items-center p-2 text-on-surface-variant hover:text-primary transition-colors" href="#">
<span class="material-symbols-outlined text-[24px]">dashboard</span>
<span class="text-[10px] font-label-md mt-1">Dash</span>
</a>
<a class="flex flex-col items-center p-2 text-primary font-bold" href="#">
<span class="material-symbols-outlined text-[24px]" style="font-variation-settings: 'FILL' 1;">warning</span>
<span class="text-[10px] font-label-md mt-1">Alerts</span>
</a>
<div class="relative -top-5">
<button class="w-12 h-12 rounded-full bg-primary text-on-primary flex items-center justify-center shadow-lg border-4 border-background">
<span class="material-symbols-outlined">add</span>
</button>
</div>
<a class="flex flex-col items-center p-2 text-on-surface-variant hover:text-primary transition-colors" href="#">
<span class="material-symbols-outlined text-[24px]">troubleshoot</span>
<span class="text-[10px] font-label-md mt-1">Data</span>
</a>
<a class="flex flex-col items-center p-2 text-on-surface-variant hover:text-primary transition-colors" href="#">
<span class="material-symbols-outlined text-[24px]">sensors</span>
<span class="text-[10px] font-label-md mt-1">Tele</span>
</a>
</nav>
</body></html>

<!-- Alerts Dashboard -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Dashboard - AgroAudit Precision</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Outfit:wght@400;500;600;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    "colors": {
                            "on-error": "#690005",
                            "on-tertiary-container": "#002d43",
                            "inverse-primary": "#006d33",
                            "background": "#0f150f",
                            "secondary-fixed-dim": "#9dd3a7",
                            "secondary-container": "#205331",
                            "surface-container-low": "#171d17",
                            "primary": "#76db8f",
                            "surface-tint": "#76db8f",
                            "on-tertiary-fixed-variant": "#004c6e",
                            "surface-variant": "#30362f",
                            "surface-dim": "#0f150f",
                            "primary-container": "#3da35d",
                            "on-primary-fixed-variant": "#005225",
                            "error-container": "#93000a",
                            "outline": "#889487",
                            "on-tertiary-fixed": "#001e2f",
                            "surface-bright": "#343b34",
                            "secondary": "#9dd3a7",
                            "on-tertiary": "#00344d",
                            "surface-container": "#1b211b",
                            "primary-fixed": "#92f8a9",
                            "secondary-fixed": "#b8f0c2",
                            "surface-container-highest": "#30362f",
                            "error": "#ffb4ab",
                            "primary-fixed-dim": "#76db8f",
                            "on-secondary-fixed": "#00210c",
                            "on-primary": "#003918",
                            "tertiary-fixed": "#c9e6ff",
                            "surface": "#0f150f",
                            "on-primary-fixed": "#00210b",
                            "outline-variant": "#3f4a3f",
                            "surface-container-lowest": "#0a100a",
                            "tertiary": "#89ceff",
                            "on-primary-container": "#003114",
                            "on-secondary-container": "#8fc599",
                            "tertiary-fixed-dim": "#89ceff",
                            "on-error-container": "#ffdad6",
                            "on-secondary": "#01391a",
                            "inverse-on-surface": "#2c322b",
                            "tertiary-container": "#009ada",
                            "on-surface": "#dee4da",
                            "surface-container-high": "#252c25",
                            "on-surface-variant": "#becabc",
                            "on-secondary-fixed-variant": "#1e502e",
                            "on-background": "#dee4da",
                            "inverse-surface": "#dee4da"
                    },
                    "borderRadius": {
                            "DEFAULT": "0.125rem",
                            "lg": "0.25rem",
                            "xl": "0.5rem",
                            "full": "0.75rem"
                    },
                    "spacing": {
                            "card-gap": "20px",
                            "gutter": "16px",
                            "container-padding": "24px",
                            "unit": "4px"
                    },
                    "fontFamily": {
                            "mono-data": [
                                    "monospace"
                            ],
                            "body-lg": [
                                    "Inter"
                            ],
                            "headline-lg": [
                                    "Outfit"
                            ],
                            "body-md": [
                                    "Inter"
                            ],
                            "label-md": [
                                    "Inter"
                            ],
                            "display-lg": [
                                    "Outfit"
                            ],
                            "body-sm": [
                                    "Inter"
                            ],
                            "headline-sm": [
                                    "Outfit"
                            ],
                            "headline-md": [
                                    "Outfit"
                            ]
                    },
                    "fontSize": {
                            "mono-data": [
                                    "14px",
                                    {
                                            "lineHeight": "20px",
                                            "fontWeight": "500"
                                    }
                            ],
                            "body-lg": [
                                    "18px",
                                    {
                                            "lineHeight": "28px",
                                            "fontWeight": "400"
                                    }
                            ],
                            "headline-lg": [
                                    "32px",
                                    {
                                            "lineHeight": "40px",
                                            "fontWeight": "600"
                                    }
                            ],
                            "body-md": [
                                    "16px",
                                    {
                                            "lineHeight": "24px",
                                            "fontWeight": "400"
                                    }
                            ],
                            "label-md": [
                                    "12px",
                                    {
                                            "lineHeight": "16px",
                                            "letterSpacing": "0.05em",
                                            "fontWeight": "600"
                                    }
                            ],
                            "display-lg": [
                                    "48px",
                                    {
                                            "lineHeight": "56px",
                                            "letterSpacing": "-0.02em",
                                            "fontWeight": "700"
                                    }
                            ],
                            "body-sm": [
                                    "14px",
                                    {
                                            "lineHeight": "20px",
                                            "fontWeight": "400"
                                    }
                            ],
                            "headline-sm": [
                                    "20px",
                                    {
                                            "lineHeight": "28px",
                                            "fontWeight": "600"
                                    }
                            ],
                            "headline-md": [
                                    "24px",
                                    {
                                            "lineHeight": "32px",
                                            "fontWeight": "600"
                                    }
                            ]
                    }
            },
                },
            }
    </script>
<style>
        /* Glassmorphism utility classes */
        .glass-panel {
            background-color: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .glass-button-primary {
            background-color: #76db8f;
            color: #003918;
            transition: all 0.2s ease-in-out;
        }
        
        .glass-button-primary:hover {
            box-shadow: 0 0 15px rgba(118, 219, 143, 0.4);
            transform: scale(0.98);
        }
        
        .glass-button-secondary {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid #76db8f;
            color: #76db8f;
            transition: all 0.2s ease-in-out;
        }
        
        .glass-button-secondary:hover {
            background-color: rgba(118, 219, 143, 0.1);
            box-shadow: 0 0 10px rgba(118, 219, 143, 0.2);
        }
        
        .pulse-border {
            animation: pulse-border-anim 2s infinite;
        }
        
        @keyframes pulse-border-anim {
            0% { border-color: rgba(255, 180, 171, 0.5); box-shadow: 0 0 0 0 rgba(255, 180, 171, 0.4); }
            70% { border-color: rgba(255, 180, 171, 1); box-shadow: 0 0 0 6px rgba(255, 180, 171, 0); }
            100% { border-color: rgba(255, 180, 171, 0.5); box-shadow: 0 0 0 0 rgba(255, 180, 171, 0); }
        }

        .table-row-hover:hover {
            background-color: rgba(255, 255, 255, 0.05);
        }
    </style>
</head>
<body class="bg-background text-on-background min-h-screen flex overflow-hidden selection:bg-primary selection:text-on-primary">
<!-- SideNavBar -->
<nav class="bg-surface/5 dark:bg-surface/5 backdrop-blur-xl h-screen w-64 fixed left-0 top-0 border-r border-white/10 hidden md:flex flex-col h-full py-6 z-40">
<!-- Header Info -->
<div class="px-6 mb-8 flex items-center gap-4">
<div class="w-10 h-10 rounded-full overflow-hidden border border-primary-container">
<img alt="System Operator" class="w-full h-full object-cover" data-alt="A macro shot of a sleek, high-tech optic lens or sensor glowing with a subtle green light, reflecting a dark, futuristic industrial environment. Clinical, sharp focus, dark background." src="https://lh3.googleusercontent.com/aida-public/AB6AXuDPtZw-aVfs6ag_9-Jud7cjdOSpnTPCod-LmSrGs5eaPSZwUQXW7y9YsRPcA0VabYzJgWtd2DrNQyW0swbpeMSZsms3C5QKwWFqSUJMmTCZB0zHggI3_4JvplqULL1Lj1_gIfupwzWcZDSpTd0NX_FVRKZWAUhGrGzjlfepA4FfA3a_0itn7IXLAQK0ZqWYx8kRj13RKsqYPHvNVrQYe-q0eYgu4wbZaPOcW5NtrbtaZJapCLfB8TCwP7Qw5rCA5udx1YxjyVxyXDM"/>
</div>
<div>
<h2 class="font-headline-sm text-headline-sm text-primary font-bold">Auditor Terminal</h2>
<p class="font-label-md text-label-md text-error mt-1 flex items-center gap-1">
<span class="w-2 h-2 rounded-full bg-error animate-pulse"></span>
                    Vigilance Level: High
                </p>
</div>
</div>
<!-- Navigation Links -->
<div class="flex-1 flex flex-col gap-2 px-4">
<a class="flex items-center gap-3 px-4 py-3 rounded-lg text-primary font-bold border-l-4 border-primary bg-white/5 transition-all duration-150" href="#">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">dashboard</span>
<span class="font-label-md text-label-md">Dashboard</span>
</a>
<a class="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:bg-white/10 transition-all duration-150 border-l-4 border-transparent" href="#">
<span class="material-symbols-outlined">warning</span>
<span class="font-label-md text-label-md">Alerts</span>
</a>
<a class="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:bg-white/10 transition-all duration-150 border-l-4 border-transparent" href="#">
<span class="material-symbols-outlined">troubleshoot</span>
<span class="font-label-md text-label-md">Data Explorer</span>
</a>
<a class="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:bg-white/10 transition-all duration-150 border-l-4 border-transparent" href="#">
<span class="material-symbols-outlined">settings</span>
<span class="font-label-md text-label-md">Configuration</span>
</a>
<a class="flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:bg-white/10 transition-all duration-150 border-l-4 border-transparent" href="#">
<span class="material-symbols-outlined">sensors</span>
<span class="font-label-md text-label-md">Telemetry</span>
</a>
</div>
<!-- CTA & Footer -->
<div class="px-4 mt-auto space-y-4">
<button class="w-full py-3 rounded-lg font-label-md text-label-md glass-button-primary flex justify-center items-center gap-2">
<span class="material-symbols-outlined text-[18px]">add</span>
                New Inspection
            </button>
<div class="pt-4 border-t border-white/10 flex flex-col gap-2">
<a class="flex items-center gap-3 px-4 py-2 rounded-lg text-on-surface-variant hover:bg-white/10 transition-all duration-150" href="#">
<span class="material-symbols-outlined text-[20px]">support_agent</span>
<span class="font-label-md text-label-md">Support</span>
</a>
<a class="flex items-center gap-3 px-4 py-2 rounded-lg text-on-surface-variant hover:bg-white/10 transition-all duration-150" href="#">
<span class="material-symbols-outlined text-[20px]">logout</span>
<span class="font-label-md text-label-md">Logout</span>
</a>
</div>
</div>
</nav>
<!-- Main Content Area -->
<main class="flex-1 flex flex-col md:ml-64 h-screen overflow-y-auto">
<!-- TopNavBar -->
<header class="bg-surface/5 dark:bg-surface/5 backdrop-blur-md w-full h-16 border-b border-white/10 flex justify-between items-center px-container-padding sticky top-0 z-50">
<div class="flex items-center gap-4">
<!-- Mobile Menu Toggle (Hidden on MD+) -->
<button class="md:hidden text-primary p-2 hover:bg-white/5 rounded-full transition-colors">
<span class="material-symbols-outlined">menu</span>
</button>
<h1 class="font-headline-sm text-headline-sm font-bold text-primary tracking-wide">AgroAudit Precision</h1>
</div>
<!-- Search Bar (on_left configuration) -->
<div class="hidden md:flex flex-1 max-w-md mx-8">
<div class="relative w-full group">
<span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant group-focus-within:text-primary transition-colors">search</span>
<input class="w-full bg-surface-container-high border border-outline-variant rounded-full py-2 pl-10 pr-4 text-body-sm font-body-sm text-on-surface focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all placeholder:text-on-surface-variant/50" placeholder="Search parameters, IDs..." type="text"/>
</div>
</div>
<!-- Trailing Actions -->
<div class="flex items-center gap-3">
<button class="w-10 h-10 rounded-full flex items-center justify-center text-on-surface-variant hover:bg-white/5 hover:text-primary transition-colors relative scale-95 hover:scale-100 duration-150">
<span class="material-symbols-outlined">notifications</span>
<span class="absolute top-2 right-2 w-2 h-2 bg-error rounded-full"></span>
</button>
<button class="w-10 h-10 rounded-full flex items-center justify-center text-on-surface-variant hover:bg-white/5 hover:text-primary transition-colors scale-95 hover:scale-100 duration-150">
<span class="material-symbols-outlined">help_outline</span>
</button>
<div class="w-8 h-8 rounded-full overflow-hidden border border-outline-variant ml-2 hidden sm:block">
<img alt="Auditor profile picture" class="w-full h-full object-cover" data-alt="A tight portrait of an auditor in a high-tech dark control room, lit by the subtle green glow of monitors. Professional, focused, sharp contrast, cinematic lighting." src="https://lh3.googleusercontent.com/aida-public/AB6AXuANFKn28Mm14RPEUQ_ejInW6AexyrL3QM27i4sPW-_CthzkZvdFm82gfrZ8RoHaz4GaPW8Mri8WK5uBmau-7a4j0PjVpWPcvtra0gOAF0Utrfi9-LJEGmdA8Mhc7F7jdIJmVOKcUxl4fwv8tMMbTwLitOGIXWDL_oCUcRTxNxaz_5I3I0JCnqu0cO7OTTGwhcl5LKcQxIBZ4CHcOkJP5kd1fOVYW6un1ipZTYZ3lmwk-PgG4REukmT2CKFoyd-Dem6bmc_Feucz3K8"/>
</div>
</div>
</header>
<!-- Page Content -->
<div class="p-container-padding flex-1 flex flex-col gap-6 max-w-[1600px] w-full mx-auto">
<!-- Page Header -->
<div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
<div>
<h2 class="font-headline-lg text-headline-lg text-on-surface">Supervision Overview</h2>
<p class="font-body-md text-body-md text-on-surface-variant mt-1">Live telemetry and anomaly detection stream.</p>
</div>
<div class="flex gap-3">
<button class="glass-button-secondary px-4 py-2 rounded-lg font-label-md text-label-md flex items-center gap-2">
<span class="material-symbols-outlined text-[18px]">download</span>
                        Export Report
                    </button>
</div>
</div>
<!-- KPI Cards Grid -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-card-gap">
<!-- KPI 1: Total Alerts -->
<div class="glass-panel rounded-xl p-5 relative overflow-hidden group">
<!-- Sparkline background decoration -->
<div class="absolute bottom-0 left-0 w-full h-1/2 opacity-20 pointer-events-none" style="background: linear-gradient(to top, #76db8f 0%, transparent 100%); clip-path: polygon(0 100%, 0 80%, 20% 70%, 40% 85%, 60% 60%, 80% 75%, 100% 40%, 100% 100%);"></div>
<div class="flex justify-between items-start mb-2 relative z-10">
<span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Total Alerts</span>
<div class="w-8 h-8 rounded-full bg-error-container/30 flex items-center justify-center text-error">
<span class="material-symbols-outlined text-[18px]">warning</span>
</div>
</div>
<div class="flex items-baseline gap-3 relative z-10">
<span class="font-display-lg text-display-lg text-on-surface">14</span>
<span class="font-body-sm text-body-sm text-error flex items-center font-medium">
<span class="material-symbols-outlined text-[16px]">trending_up</span>
                            +5%
                        </span>
</div>
</div>
<!-- KPI 2: Operations Analyzed -->
<div class="glass-panel rounded-xl p-5 relative overflow-hidden group">
<div class="absolute bottom-0 left-0 w-full h-1/2 opacity-10 pointer-events-none" style="background: linear-gradient(to top, #ffffff 0%, transparent 100%); clip-path: polygon(0 100%, 0 90%, 30% 80%, 50% 85%, 70% 60%, 90% 70%, 100% 50%, 100% 100%);"></div>
<div class="flex justify-between items-start mb-2 relative z-10">
<span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Operations Analyzed</span>
<div class="w-8 h-8 rounded-full bg-surface-bright flex items-center justify-center text-on-surface-variant">
<span class="material-symbols-outlined text-[18px]">query_stats</span>
</div>
</div>
<div class="flex items-baseline gap-3 relative z-10">
<span class="font-display-lg text-display-lg text-on-surface">1,240</span>
<span class="font-body-sm text-body-sm text-primary flex items-center font-medium">
                            Daily Vol.
                        </span>
</div>
</div>
<!-- KPI 3: F1-Score -->
<div class="glass-panel rounded-xl p-5 relative overflow-hidden group">
<div class="absolute bottom-0 left-0 w-full h-1/2 opacity-20 pointer-events-none" style="background: linear-gradient(to top, #76db8f 0%, transparent 100%); clip-path: polygon(0 100%, 0 50%, 40% 45%, 60% 30%, 80% 35%, 100% 20%, 100% 100%);"></div>
<div class="flex justify-between items-start mb-2 relative z-10">
<span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Model F1-Score</span>
<div class="w-8 h-8 rounded-full bg-primary-container/20 flex items-center justify-center text-primary">
<span class="material-symbols-outlined text-[18px]">precision_manufacturing</span>
</div>
</div>
<div class="flex items-baseline gap-3 relative z-10">
<span class="font-display-lg text-display-lg text-on-surface">0.92</span>
<span class="font-body-sm text-body-sm text-on-surface-variant flex items-center">
                            High Confidence
                        </span>
</div>
</div>
<!-- KPI 4: Avg Decision Time -->
<div class="glass-panel rounded-xl p-5 relative overflow-hidden group">
<div class="flex justify-between items-start mb-2 relative z-10">
<span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Avg. Decision Time</span>
<div class="w-8 h-8 rounded-full bg-surface-bright flex items-center justify-center text-on-surface-variant">
<span class="material-symbols-outlined text-[18px]">timer</span>
</div>
</div>
<div class="flex items-baseline gap-3 relative z-10">
<span class="font-display-lg text-display-lg text-on-surface">42s</span>
<span class="font-body-sm text-body-sm text-primary flex items-center font-medium">
<span class="material-symbols-outlined text-[16px]">trending_down</span>
                            -2s
                        </span>
</div>
</div>
</div>
<!-- Filters & Main Table Section -->
<div class="glass-panel rounded-xl flex-1 flex flex-col overflow-hidden">
<!-- Toolbar / Filters -->
<div class="p-4 border-b border-white/10 flex flex-wrap items-center gap-4 bg-surface-container-low/50">
<div class="font-headline-sm text-headline-sm text-on-surface mr-auto flex items-center gap-2">
<span class="material-symbols-outlined text-primary">format_list_bulleted</span>
                        Active Alerts Queue
                    </div>
<!-- Filters -->
<div class="flex flex-wrap gap-3">
<div class="relative">
<select class="appearance-none bg-surface border border-outline-variant rounded-lg py-2 pl-4 pr-10 font-body-sm text-body-sm text-on-surface focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary cursor-pointer">
<option value="">Product: All</option>
<option value="palta">Palta</option>
<option value="uva">Uva</option>
<option value="arandano">Arándano</option>
</select>
<span class="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-on-surface-variant">arrow_drop_down</span>
</div>
<div class="relative">
<select class="appearance-none bg-surface border border-outline-variant rounded-lg py-2 pl-4 pr-10 font-body-sm text-body-sm text-on-surface focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary cursor-pointer">
<option value="">Status: All</option>
<option value="pending">Pending</option>
<option value="resolved">Resolved</option>
<option value="escalated">Escalated</option>
</select>
<span class="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-on-surface-variant">arrow_drop_down</span>
</div>
</div>
</div>
<!-- Table Container -->
<div class="overflow-x-auto">
<table class="w-full text-left border-collapse min-w-[800px]">
<thead>
<tr class="bg-surface-container-low/80 border-b border-primary/50">
<th class="py-3 px-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Alert ID</th>
<th class="py-3 px-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Date/Time</th>
<th class="py-3 px-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Product</th>
<th class="py-3 px-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Exporter / Route</th>
<th class="py-3 px-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider w-48">Anomaly Score</th>
<th class="py-3 px-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Status</th>
<th class="py-3 px-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider text-right">Action</th>
</tr>
</thead>
<tbody class="divide-y divide-white/5 bg-[rgba(255,255,255,0.02)]">
<!-- High Priority Row -->
<tr class="table-row-hover transition-colors group">
<td class="py-4 px-4">
<div class="flex items-center gap-2">
<div class="w-2 h-2 rounded-full bg-error animate-pulse"></div>
<span class="font-mono-data text-mono-data text-on-surface">AL-2026-0012</span>
</div>
</td>
<td class="py-4 px-4 font-body-sm text-body-sm text-on-surface-variant">Oct 24, 14:32:05</td>
<td class="py-4 px-4 font-body-sm text-body-sm text-on-surface">Arándano</td>
<td class="py-4 px-4">
<div class="font-body-sm text-body-sm text-on-surface">Exportadora Del Sur SAC</div>
<div class="font-label-md text-label-md text-on-surface-variant flex items-center gap-1 mt-1">
<span class="material-symbols-outlined text-[14px]">flight_takeoff</span>
                                        Port of Rotterdam
                                    </div>
</td>
<td class="py-4 px-4">
<div class="flex items-center gap-2">
<span class="font-mono-data text-mono-data text-error font-bold w-8">89%</span>
<div class="flex-1 h-2 bg-surface rounded-full overflow-hidden border border-white/10">
<div class="h-full bg-error rounded-full" style="width: 89%;"></div>
</div>
</div>
</td>
<td class="py-4 px-4">
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full font-label-md text-label-md bg-error-container/30 text-error border border-error/30 pulse-border">
                                        PENDING
                                    </span>
</td>
<td class="py-4 px-4 text-right">
<button class="glass-button-primary px-4 py-1.5 rounded-lg font-label-md text-label-md font-bold opacity-0 group-hover:opacity-100 transition-opacity focus:opacity-100">
                                        Audit
                                    </button>
</td>
</tr>
<!-- Medium Priority Row -->
<tr class="table-row-hover transition-colors group">
<td class="py-4 px-4">
<div class="flex items-center gap-2">
<div class="w-2 h-2 rounded-full bg-primary"></div>
<span class="font-mono-data text-mono-data text-on-surface">AL-2026-0011</span>
</div>
</td>
<td class="py-4 px-4 font-body-sm text-body-sm text-on-surface-variant">Oct 24, 14:15:22</td>
<td class="py-4 px-4 font-body-sm text-body-sm text-on-surface">Palta</td>
<td class="py-4 px-4">
<div class="font-body-sm text-body-sm text-on-surface">Agro Industrias Norte</div>
<div class="font-label-md text-label-md text-on-surface-variant flex items-center gap-1 mt-1">
<span class="material-symbols-outlined text-[14px]">sailing</span>
                                        Port of Los Angeles
                                    </div>
</td>
<td class="py-4 px-4">
<div class="flex items-center gap-2">
<span class="font-mono-data text-mono-data text-primary font-bold w-8">62%</span>
<div class="flex-1 h-2 bg-surface rounded-full overflow-hidden border border-white/10">
<div class="h-full bg-primary rounded-full" style="width: 62%;"></div>
</div>
</div>
</td>
<td class="py-4 px-4">
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full font-label-md text-label-md bg-surface-bright text-on-surface border border-outline-variant">
                                        INVESTIGATING
                                    </span>
</td>
<td class="py-4 px-4 text-right">
<button class="glass-button-secondary px-4 py-1.5 rounded-lg font-label-md text-label-md opacity-0 group-hover:opacity-100 transition-opacity focus:opacity-100">
                                        Review
                                    </button>
</td>
</tr>
<!-- Low Priority Row -->
<tr class="table-row-hover transition-colors group">
<td class="py-4 px-4">
<div class="flex items-center gap-2">
<div class="w-2 h-2 rounded-full bg-outline"></div>
<span class="font-mono-data text-mono-data text-on-surface">AL-2026-0010</span>
</div>
</td>
<td class="py-4 px-4 font-body-sm text-body-sm text-on-surface-variant">Oct 24, 13:50:10</td>
<td class="py-4 px-4 font-body-sm text-body-sm text-on-surface">Uva</td>
<td class="py-4 px-4">
<div class="font-body-sm text-body-sm text-on-surface">Viñedos de Ica S.A.</div>
<div class="font-label-md text-label-md text-on-surface-variant flex items-center gap-1 mt-1">
<span class="material-symbols-outlined text-[14px]">sailing</span>
                                        Port of Shanghai
                                    </div>
</td>
<td class="py-4 px-4">
<div class="flex items-center gap-2">
<span class="font-mono-data text-mono-data text-outline font-bold w-8">35%</span>
<div class="flex-1 h-2 bg-surface rounded-full overflow-hidden border border-white/10">
<div class="h-full bg-outline rounded-full" style="width: 35%;"></div>
</div>
</div>
</td>
<td class="py-4 px-4">
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full font-label-md text-label-md bg-surface-bright text-on-surface border border-outline-variant">
                                        LOGGED
                                    </span>
</td>
<td class="py-4 px-4 text-right">
<button class="glass-button-secondary px-4 py-1.5 rounded-lg font-label-md text-label-md opacity-0 group-hover:opacity-100 transition-opacity focus:opacity-100">
                                        Details
                                    </button>
</td>
</tr>
</tbody>
</table>
</div>
</div>
</div>
</main>
</body></html>

<!-- Telemetry & Fairness Monitor -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Telemetry Panel - AgroAudit Precision</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    "colors": {
                        "on-error": "#690005",
                        "on-tertiary-container": "#002d43",
                        "inverse-primary": "#006d33",
                        "background": "#0f150f",
                        "secondary-fixed-dim": "#9dd3a7",
                        "secondary-container": "#205331",
                        "surface-container-low": "#171d17",
                        "primary": "#76db8f",
                        "surface-tint": "#76db8f",
                        "on-tertiary-fixed-variant": "#004c6e",
                        "surface-variant": "#30362f",
                        "surface-dim": "#0f150f",
                        "primary-container": "#3da35d",
                        "on-primary-fixed-variant": "#005225",
                        "error-container": "#93000a",
                        "outline": "#889487",
                        "on-tertiary-fixed": "#001e2f",
                        "surface-bright": "#343b34",
                        "secondary": "#9dd3a7",
                        "on-tertiary": "#00344d",
                        "surface-container": "#1b211b",
                        "primary-fixed": "#92f8a9",
                        "secondary-fixed": "#b8f0c2",
                        "surface-container-highest": "#30362f",
                        "error": "#ffb4ab",
                        "primary-fixed-dim": "#76db8f",
                        "on-secondary-fixed": "#00210c",
                        "on-primary": "#003918",
                        "tertiary-fixed": "#c9e6ff",
                        "surface": "#0f150f",
                        "on-primary-fixed": "#00210b",
                        "outline-variant": "#3f4a3f",
                        "surface-container-lowest": "#0a100a",
                        "tertiary": "#89ceff",
                        "on-primary-container": "#003114",
                        "on-secondary-container": "#8fc599",
                        "tertiary-fixed-dim": "#89ceff",
                        "on-error-container": "#ffdad6",
                        "on-secondary": "#01391a",
                        "inverse-on-surface": "#2c322b",
                        "tertiary-container": "#009ada",
                        "on-surface": "#dee4da",
                        "surface-container-high": "#252c25",
                        "on-surface-variant": "#becabc",
                        "on-secondary-fixed-variant": "#1e502e",
                        "on-background": "#dee4da",
                        "inverse-surface": "#dee4da"
                    },
                    "borderRadius": {
                        "DEFAULT": "0.125rem",
                        "lg": "0.25rem",
                        "xl": "0.5rem",
                        "full": "0.75rem"
                    },
                    "spacing": {
                        "card-gap": "20px",
                        "gutter": "16px",
                        "container-padding": "24px",
                        "unit": "4px"
                    },
                    "fontFamily": {
                        "mono-data": ["monospace"],
                        "body-lg": ["Inter", "sans-serif"],
                        "headline-lg": ["Outfit", "sans-serif"],
                        "body-md": ["Inter", "sans-serif"],
                        "label-md": ["Inter", "sans-serif"],
                        "display-lg": ["Outfit", "sans-serif"],
                        "body-sm": ["Inter", "sans-serif"],
                        "headline-sm": ["Outfit", "sans-serif"],
                        "headline-md": ["Outfit", "sans-serif"]
                    },
                    "fontSize": {
                        "mono-data": ["14px", { "lineHeight": "20px", "fontWeight": "500" }],
                        "body-lg": ["18px", { "lineHeight": "28px", "fontWeight": "400" }],
                        "headline-lg": ["32px", { "lineHeight": "40px", "fontWeight": "600" }],
                        "body-md": ["16px", { "lineHeight": "24px", "fontWeight": "400" }],
                        "label-md": ["12px", { "lineHeight": "16px", "letterSpacing": "0.05em", "fontWeight": "600" }],
                        "display-lg": ["48px", { "lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "700" }],
                        "body-sm": ["14px", { "lineHeight": "20px", "fontWeight": "400" }],
                        "headline-sm": ["20px", { "lineHeight": "28px", "fontWeight": "600" }],
                        "headline-md": ["24px", { "lineHeight": "32px", "fontWeight": "600" }]
                    }
                }
            }
        }
    </script>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Outfit:wght@600;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<style>
        /* Glassmorphism utility classes */
        .glass-panel {
            background-color: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .glass-button {
            background-color: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(118, 219, 143, 0.5); /* Emerald border */
            transition: all 0.2s ease;
        }
        
        .glass-button:hover {
            box-shadow: 0 0 15px rgba(118, 219, 143, 0.3);
            background-color: rgba(255, 255, 255, 0.1);
        }

        .primary-button {
            background-color: #76db8f;
            color: #003918;
            transition: all 0.2s ease;
        }
        
        .primary-button:hover {
            background-color: #92f8a9;
            box-shadow: 0 0 20px rgba(118, 219, 143, 0.4);
        }

        /* Chart mockups */
        .bar-chart-bar {
            background: linear-gradient(to top, rgba(118, 219, 143, 0.8), rgba(118, 219, 143, 0.2));
            transition: height 1s ease-in-out;
        }
        .bar-chart-bar-alt {
            background: linear-gradient(to top, rgba(137, 206, 255, 0.8), rgba(137, 206, 255, 0.2));
            transition: height 1s ease-in-out;
        }

        /* Zebra striping for tables */
        .table-row-zebra:nth-child(even) {
            background-color: rgba(255, 255, 255, 0.02);
        }

        /* Scrollbar styling for data tables */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.02); 
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.1); 
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.2); 
        }
    </style>
</head>
<body class="bg-background text-on-surface min-h-screen flex overflow-hidden">
<!-- SideNavBar -->
<nav class="hidden md:flex flex-col h-screen w-64 fixed left-0 top-0 bg-surface/5 dark:bg-surface/5 backdrop-blur-xl border-r border-white/10 py-6 z-40">
<!-- Header -->
<div class="px-6 mb-8">
<div class="flex items-center gap-3 mb-4">
<div class="w-10 h-10 rounded-full overflow-hidden border border-outline/30 relative">
<img alt="System Operator" class="object-cover w-full h-full" data-alt="A close-up, high-tech stylized portrait of a system operator in a dark, clinical control room. Soft emerald lighting reflects off a glass visor. The mood is vigilant and precise. Deep charcoal and dark green tones dominate the palette, adhering to a sophisticated dark-glassmorphism aesthetic." src="https://lh3.googleusercontent.com/aida-public/AB6AXuAkzMkiInpPtge4zy_e_Mq6OwVpDuV7zi27VBcSt6wX91-8tOhdu5gdWt4TO2upA9juVlo_qlMJ6hXTthx7-J27rUdOREQPux8RtMz_zFauiUgh2io2r4vxQXFciHtfmRO7dBpxdZRsKO4zmgp4utsYkwQXC6_NSgr2hxZCGGH3xpiusqLruIZqxzs7MgBcyZfJDqRpLeMys3xaQDpx30DoK3CCfCRbdvbjRDd7kzVTLnWjrpAwrnYvks8l91IKc9fbxxt_OJn22jo"/>
</div>
<div>
<h2 class="font-headline-sm text-headline-sm text-primary">Auditor Terminal</h2>
<p class="font-label-md text-label-md text-on-surface-variant">Vigilance Level: High</p>
</div>
</div>
<button class="w-full primary-button font-label-md text-label-md rounded py-2 px-4 flex items-center justify-center gap-2">
<span class="material-symbols-outlined text-[18px]">add</span>
                New Inspection
            </button>
</div>
<!-- Navigation Links -->
<div class="flex-1 px-4 space-y-1">
<a class="flex items-center gap-3 px-4 py-3 rounded text-on-surface-variant hover:bg-white/10 transition-all font-label-md text-label-md" href="#">
<span class="material-symbols-outlined">dashboard</span>
                Dashboard
            </a>
<a class="flex items-center gap-3 px-4 py-3 rounded text-on-surface-variant hover:bg-white/10 transition-all font-label-md text-label-md" href="#">
<span class="material-symbols-outlined">warning</span>
                Alerts
            </a>
<a class="flex items-center gap-3 px-4 py-3 rounded text-on-surface-variant hover:bg-white/10 transition-all font-label-md text-label-md" href="#">
<span class="material-symbols-outlined">troubleshoot</span>
                Data Explorer
            </a>
<a class="flex items-center gap-3 px-4 py-3 rounded text-on-surface-variant hover:bg-white/10 transition-all font-label-md text-label-md" href="#">
<span class="material-symbols-outlined">settings</span>
                Configuration
            </a>
<!-- Active State -->
<a class="flex items-center gap-3 px-4 py-3 rounded text-primary font-bold border-l-4 border-primary bg-white/5 hover:bg-white/10 transition-all font-label-md text-label-md translate-x-1 duration-200" href="#">
<span class="material-symbols-outlined">sensors</span>
                Telemetry
            </a>
</div>
<!-- Footer Links -->
<div class="px-4 mt-auto space-y-1 border-t border-white/10 pt-4">
<a class="flex items-center gap-3 px-4 py-2 rounded text-on-surface-variant hover:bg-white/10 transition-all font-label-md text-label-md" href="#">
<span class="material-symbols-outlined">support_agent</span>
                Support
            </a>
<a class="flex items-center gap-3 px-4 py-2 rounded text-on-surface-variant hover:bg-white/10 transition-all font-label-md text-label-md" href="#">
<span class="material-symbols-outlined">logout</span>
                Logout
            </a>
</div>
</nav>
<!-- Main Content Canvas -->
<main class="flex-1 md:ml-64 h-screen overflow-y-auto overflow-x-hidden relative">
<!-- TopNavBar (Mobile mainly, but keeping structural intent for responsiveness) -->
<header class="flex justify-between items-center px-container-padding w-full sticky top-0 z-50 h-16 bg-surface/5 dark:bg-surface/5 backdrop-blur-md border-b border-white/10 md:hidden">
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-primary">eco</span>
<span class="font-headline-sm text-headline-sm font-bold text-primary">AgroAudit Precision</span>
</div>
<div class="flex items-center gap-4">
<button class="text-on-surface-variant hover:bg-white/5 transition-colors p-2 rounded-full scale-95 duration-150">
<span class="material-symbols-outlined">notifications</span>
</button>
<button class="text-on-surface-variant hover:bg-white/5 transition-colors p-2 rounded-full scale-95 duration-150">
<span class="material-symbols-outlined">help_outline</span>
</button>
</div>
</header>
<!-- Dashboard Content -->
<div class="p-container-padding max-w-[1600px] mx-auto space-y-card-gap pb-24">
<!-- Page Header & Actions -->
<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
<div>
<h1 class="font-headline-lg text-headline-lg text-on-surface">Telemetry &amp; Experimental Results</h1>
<p class="font-body-md text-body-md text-on-surface-variant mt-1">Admin Panel: Thesis Analysis Dashboard</p>
</div>
<div class="flex items-center gap-3">
<button class="glass-button font-label-md text-label-md text-primary px-4 py-2 rounded flex items-center gap-2">
<span class="material-symbols-outlined text-[18px]">download</span>
                        Export to CSV
                    </button>
</div>
</div>
<!-- Bento Grid Layout -->
<div class="grid grid-cols-1 lg:grid-cols-12 gap-card-gap">
<!-- Time-to-Decision Comparison (Chart 1) -->
<div class="glass-panel rounded-xl p-6 lg:col-span-8 flex flex-col min-h-[350px]">
<div class="flex justify-between items-start mb-6">
<div>
<h3 class="font-headline-sm text-headline-sm text-on-surface">Time-to-Decision Comparison</h3>
<p class="font-body-sm text-body-sm text-on-surface-variant">Condition A (Baseline) vs Condition B (Enhanced)</p>
</div>
<span class="material-symbols-outlined text-on-surface-variant">monitoring</span>
</div>
<div class="flex-1 relative flex items-end justify-around pb-8 px-4 border-b border-white/10 mt-4">
<!-- Y-axis labels -->
<div class="absolute left-0 top-0 h-full flex flex-col justify-between text-on-surface-variant font-mono-data text-mono-data text-xs pb-8">
<span>1500ms</span>
<span>1000ms</span>
<span>500ms</span>
<span>0ms</span>
</div>
<!-- Chart Area -->
<div class="w-full h-full flex justify-around items-end ml-10">
<!-- Condition A -->
<div class="flex flex-col items-center gap-2">
<div class="w-16 sm:w-24 h-[60%] bar-chart-bar-alt rounded-t relative group">
<div class="absolute -top-8 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity bg-surface-container-high px-2 py-1 rounded font-mono-data text-mono-data text-xs border border-white/10">950ms</div>
</div>
<span class="font-label-md text-label-md text-on-surface mt-2">Condition A</span>
</div>
<!-- Condition B -->
<div class="flex flex-col items-center gap-2">
<div class="w-16 sm:w-24 h-[40%] bar-chart-bar rounded-t relative group">
<div class="absolute -top-8 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity bg-surface-container-high px-2 py-1 rounded font-mono-data text-mono-data text-xs border border-white/10">620ms</div>
</div>
<span class="font-label-md text-label-md text-on-surface mt-2">Condition B</span>
</div>
</div>
</div>
</div>
<!-- KPI Cards (Col-span-4) -->
<div class="lg:col-span-4 flex flex-col gap-card-gap">
<!-- KPI 1 -->
<div class="glass-panel rounded-xl p-6 flex-1 flex flex-col justify-center relative overflow-hidden">
<div class="absolute inset-0 opacity-10 pointer-events-none" style="background-image: radial-gradient(circle at right bottom, #76db8f 0%, transparent 50%);"></div>
<h4 class="font-body-sm text-body-sm text-on-surface-variant mb-2">Avg. Comprehension Score</h4>
<div class="font-display-lg text-display-lg text-primary">89.4%</div>
<div class="flex items-center gap-1 mt-2 text-primary">
<span class="material-symbols-outlined text-[16px]">trending_up</span>
<span class="font-label-md text-label-md">+4.2% vs Baseline</span>
</div>
</div>
<!-- KPI 2 -->
<div class="glass-panel rounded-xl p-6 flex-1 flex flex-col justify-center relative overflow-hidden">
<div class="absolute inset-0 opacity-10 pointer-events-none" style="background-image: radial-gradient(circle at right bottom, #89ceff 0%, transparent 50%);"></div>
<h4 class="font-body-sm text-body-sm text-on-surface-variant mb-2">Total Decisions Logged</h4>
<div class="font-display-lg text-display-lg text-tertiary">14,208</div>
<div class="flex items-center gap-1 mt-2 text-on-surface-variant">
<span class="font-label-md text-label-md">Across 4 experimental variants</span>
</div>
</div>
</div>
<!-- Fairness Monitor (Chart 2) -->
<div class="glass-panel rounded-xl p-6 lg:col-span-6 min-h-[300px] flex flex-col">
<div class="flex justify-between items-start mb-6">
<div>
<h3 class="font-headline-sm text-headline-sm text-on-surface">Fairness Monitor</h3>
<p class="font-body-sm text-body-sm text-on-surface-variant">False Positive Rates by Product Category</p>
</div>
<span class="material-symbols-outlined text-on-surface-variant">balance</span>
</div>
<div class="flex-1 flex flex-col justify-end gap-4 mt-4">
<!-- Palta -->
<div class="w-full">
<div class="flex justify-between text-xs mb-1">
<span class="font-label-md text-label-md text-on-surface">Palta (Avocado)</span>
<span class="font-mono-data text-mono-data text-on-surface-variant">2.4%</span>
</div>
<div class="h-2 w-full bg-white/5 rounded-full overflow-hidden">
<div class="h-full bg-primary" style="width: 24%;"></div>
</div>
</div>
<!-- Uva -->
<div class="w-full">
<div class="flex justify-between text-xs mb-1">
<span class="font-label-md text-label-md text-on-surface">Uva (Grape)</span>
<span class="font-mono-data text-mono-data text-on-surface-variant">1.8%</span>
</div>
<div class="h-2 w-full bg-white/5 rounded-full overflow-hidden">
<div class="h-full bg-tertiary" style="width: 18%;"></div>
</div>
</div>
<!-- Arandano -->
<div class="w-full">
<div class="flex justify-between text-xs mb-1">
<span class="font-label-md text-label-md text-on-surface">Arándano (Blueberry)</span>
<span class="font-mono-data text-mono-data text-on-surface-variant">3.1%</span>
</div>
<div class="h-2 w-full bg-white/5 rounded-full overflow-hidden">
<div class="h-full bg-error" style="width: 31%;"></div>
</div>
</div>
<!-- Mango -->
<div class="w-full">
<div class="flex justify-between text-xs mb-1">
<span class="font-label-md text-label-md text-on-surface">Mango</span>
<span class="font-mono-data text-mono-data text-on-surface-variant">2.1%</span>
</div>
<div class="h-2 w-full bg-white/5 rounded-full overflow-hidden">
<div class="h-full bg-secondary" style="width: 21%;"></div>
</div>
</div>
</div>
</div>
<!-- Scatter Plot Mockup (Chart 3) -->
<div class="glass-panel rounded-xl p-6 lg:col-span-6 min-h-[300px] flex flex-col relative overflow-hidden">
<div class="flex justify-between items-start z-10 relative">
<div>
<h3 class="font-headline-sm text-headline-sm text-on-surface">Accuracy vs. Decision Time</h3>
<p class="font-body-sm text-body-sm text-on-surface-variant">Distribution across user responses</p>
</div>
<span class="material-symbols-outlined text-on-surface-variant">scatter_plot</span>
</div>
<!-- Decorative Scatter Visual (Abstract representation) -->
<div class="absolute inset-0 pt-20 pb-6 px-6 z-0">
<div class="w-full h-full border-l border-b border-white/10 relative">
<!-- Axis labels -->
<span class="absolute -bottom-6 left-1/2 -translate-x-1/2 font-label-md text-label-md text-on-surface-variant text-[10px]">Decision Time (ms)</span>
<span class="absolute top-1/2 -left-6 -translate-y-1/2 -rotate-90 font-label-md text-label-md text-on-surface-variant text-[10px] whitespace-nowrap">Accuracy (%)</span>
<!-- Dots (High accuracy, fast time cluster - Condition B) -->
<div class="absolute bottom-[80%] left-[20%] w-2 h-2 rounded-full bg-primary/80 shadow-[0_0_8px_rgba(118,219,143,0.8)]"></div>
<div class="absolute bottom-[85%] left-[25%] w-1.5 h-1.5 rounded-full bg-primary/60"></div>
<div class="absolute bottom-[75%] left-[15%] w-2.5 h-2.5 rounded-full bg-primary/70"></div>
<div class="absolute bottom-[90%] left-[30%] w-1 h-1 rounded-full bg-primary/90"></div>
<div class="absolute bottom-[82%] left-[22%] w-2 h-2 rounded-full bg-primary/80 shadow-[0_0_8px_rgba(118,219,143,0.8)]"></div>
<!-- Dots (Lower accuracy, slower time cluster - Condition A) -->
<div class="absolute bottom-[50%] left-[60%] w-2 h-2 rounded-full bg-tertiary/80 shadow-[0_0_8px_rgba(137,206,255,0.8)]"></div>
<div class="absolute bottom-[45%] left-[65%] w-1.5 h-1.5 rounded-full bg-tertiary/60"></div>
<div class="absolute bottom-[55%] left-[55%] w-2.5 h-2.5 rounded-full bg-tertiary/70"></div>
<div class="absolute bottom-[40%] left-[70%] w-1 h-1 rounded-full bg-tertiary/90"></div>
<div class="absolute bottom-[48%] left-[62%] w-2 h-2 rounded-full bg-tertiary/80"></div>
<!-- Trend Line Approximation -->
<svg class="absolute inset-0 w-full h-full" preserveaspectratio="none">
<line stroke="rgba(255,255,255,0.1)" stroke-dasharray="4" stroke-width="1" x1="10%" x2="90%" y1="90%" y2="20%"></line>
</svg>
</div>
</div>
</div>
<!-- Full Telemetry Logs Table -->
<div class="glass-panel rounded-xl lg:col-span-12 flex flex-col overflow-hidden">
<div class="p-6 border-b border-white/10 flex justify-between items-center bg-white/5">
<h3 class="font-headline-sm text-headline-sm text-on-surface">Full Telemetry Logs</h3>
<div class="flex items-center gap-2">
<span class="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
<span class="font-mono-data text-mono-data text-on-surface-variant text-xs">Live Stream Active</span>
</div>
</div>
<div class="overflow-x-auto">
<table class="w-full text-left border-collapse min-w-[800px]">
<thead>
<tr class="border-b border-primary/50 bg-white/5">
<th class="p-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">User ID</th>
<th class="p-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Alert ID</th>
<th class="p-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Condition</th>
<th class="p-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Decision</th>
<th class="p-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Comp. Score</th>
<th class="p-4 font-label-md text-label-md text-on-surface-variant uppercase tracking-wider text-right">Time (ms)</th>
</tr>
</thead>
<tbody class="font-mono-data text-mono-data">
<tr class="table-row-zebra border-b border-white/5 hover:bg-white/5 transition-colors">
<td class="p-4 text-on-surface">USR-8821</td>
<td class="p-4 text-on-surface-variant">ALT-992-P</td>
<td class="p-4"><span class="px-2 py-1 bg-primary/10 text-primary rounded border border-primary/20 text-xs">B (Enhanced)</span></td>
<td class="p-4 text-on-surface">Reject</td>
<td class="p-4 text-primary">95%</td>
<td class="p-4 text-right text-on-surface">642</td>
</tr>
<tr class="table-row-zebra border-b border-white/5 hover:bg-white/5 transition-colors">
<td class="p-4 text-on-surface">USR-8845</td>
<td class="p-4 text-on-surface-variant">ALT-104-U</td>
<td class="p-4"><span class="px-2 py-1 bg-tertiary/10 text-tertiary rounded border border-tertiary/20 text-xs">A (Baseline)</span></td>
<td class="p-4 text-on-surface">Approve</td>
<td class="p-4 text-outline">78%</td>
<td class="p-4 text-right text-on-surface">1205</td>
</tr>
<tr class="table-row-zebra border-b border-white/5 hover:bg-white/5 transition-colors">
<td class="p-4 text-on-surface">USR-8821</td>
<td class="p-4 text-on-surface-variant">ALT-993-M</td>
<td class="p-4"><span class="px-2 py-1 bg-primary/10 text-primary rounded border border-primary/20 text-xs">B (Enhanced)</span></td>
<td class="p-4 text-on-surface">Escalate</td>
<td class="p-4 text-primary">92%</td>
<td class="p-4 text-right text-on-surface">710</td>
</tr>
<tr class="table-row-zebra border-b border-white/5 hover:bg-white/5 transition-colors">
<td class="p-4 text-on-surface">USR-8810</td>
<td class="p-4 text-on-surface-variant">ALT-201-A</td>
<td class="p-4"><span class="px-2 py-1 bg-tertiary/10 text-tertiary rounded border border-tertiary/20 text-xs">A (Baseline)</span></td>
<td class="p-4 text-on-surface">Reject</td>
<td class="p-4 text-error">45%</td>
<td class="p-4 text-right text-on-surface">1850</td>
</tr>
<tr class="table-row-zebra hover:bg-white/5 transition-colors">
<td class="p-4 text-on-surface">USR-8899</td>
<td class="p-4 text-on-surface-variant">ALT-442-P</td>
<td class="p-4"><span class="px-2 py-1 bg-primary/10 text-primary rounded border border-primary/20 text-xs">B (Enhanced)</span></td>
<td class="p-4 text-on-surface">Approve</td>
<td class="p-4 text-primary">88%</td>
<td class="p-4 text-right text-on-surface">590</td>
</tr>
</tbody>
</table>
</div>
</div>
</div>
</div>
</main>
</body></html>

<!-- Model Configuration Terminal -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Model Configuration &amp; Pipeline Management - Agro-Intelligence Oversight</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&amp;family=Inter:wght@400;500;600&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            "colors": {
                    "outline-variant": "#3f4a3f",
                    "surface-container-low": "#171d17",
                    "primary-container": "#3da35d",
                    "surface-container-lowest": "#0a100a",
                    "on-secondary-fixed-variant": "#1e502e",
                    "inverse-on-surface": "#2c322b",
                    "surface-container": "#1b211b",
                    "surface-variant": "#30362f",
                    "surface-container-highest": "#30362f",
                    "inverse-primary": "#006d33",
                    "primary-fixed": "#92f8a9",
                    "on-surface-variant": "#becabc",
                    "tertiary-fixed-dim": "#89ceff",
                    "on-surface": "#dee4da",
                    "surface-tint": "#76db8f",
                    "tertiary-fixed": "#c9e6ff",
                    "on-error-container": "#ffdad6",
                    "on-tertiary-fixed": "#001e2f",
                    "on-background": "#dee4da",
                    "on-tertiary-fixed-variant": "#004c6e",
                    "error-container": "#93000a",
                    "secondary-container": "#205331",
                    "primary-fixed-dim": "#76db8f",
                    "on-secondary-container": "#8fc599",
                    "on-primary-container": "#003114",
                    "tertiary": "#89ceff",
                    "surface-bright": "#343b34",
                    "secondary": "#9dd3a7",
                    "on-primary-fixed": "#00210b",
                    "on-tertiary": "#00344d",
                    "on-primary": "#003918",
                    "secondary-fixed": "#b8f0c2",
                    "background": "#0f150f",
                    "outline": "#889487",
                    "tertiary-container": "#009ada",
                    "primary": "#76db8f",
                    "on-tertiary-container": "#002d43",
                    "surface-container-high": "#252c25",
                    "surface-dim": "#0f150f",
                    "on-error": "#690005",
                    "inverse-surface": "#dee4da",
                    "surface": "#0f150f",
                    "on-secondary-fixed": "#00210c",
                    "on-primary-fixed-variant": "#005225",
                    "on-secondary": "#01391a",
                    "secondary-fixed-dim": "#9dd3a7",
                    "error": "#ffb4ab"
            },
            "borderRadius": {
                    "DEFAULT": "0.125rem",
                    "lg": "0.25rem",
                    "xl": "0.5rem",
                    "full": "0.75rem"
            },
            "spacing": {
                    "gutter": "16px",
                    "card-gap": "20px",
                    "container-padding": "24px",
                    "unit": "4px"
            },
            "fontFamily": {
                    "body-md": ["Inter"],
                    "headline-sm": ["Outfit"],
                    "body-sm": ["Inter"],
                    "headline-md": ["Outfit"],
                    "display-lg": ["Outfit"],
                    "headline-lg": ["Outfit"],
                    "mono-data": ["monospace"],
                    "label-md": ["Inter"],
                    "body-lg": ["Inter"]
            },
            "fontSize": {
                    "body-md": ["16px", {"lineHeight": "24px", "fontWeight": "400"}],
                    "headline-sm": ["20px", {"lineHeight": "28px", "fontWeight": "600"}],
                    "body-sm": ["14px", {"lineHeight": "20px", "fontWeight": "400"}],
                    "headline-md": ["24px", {"lineHeight": "32px", "fontWeight": "600"}],
                    "display-lg": ["48px", {"lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "700"}],
                    "headline-lg": ["32px", {"lineHeight": "40px", "fontWeight": "600"}],
                    "mono-data": ["14px", {"lineHeight": "20px", "fontWeight": "500"}],
                    "label-md": ["12px", {"lineHeight": "16px", "letterSpacing": "0.05em", "fontWeight": "600"}],
                    "body-lg": ["18px", {"lineHeight": "28px", "fontWeight": "400"}]
            }
          }
        }
      }
    </script>
<style>
        .glass-panel {
            background-color: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .glass-panel:hover {
            border-color: rgba(118, 219, 143, 0.3); /* Primary color low opacity */
        }
        .data-value {
            font-family: monospace;
        }
        
        /* Custom Range Slider Styling */
        input[type=range] {
            -webkit-appearance: none;
            width: 100%;
            background: transparent;
        }
        input[type=range]::-webkit-slider-thumb {
            -webkit-appearance: none;
            height: 16px;
            width: 16px;
            border-radius: 50%;
            background: #76db8f; /* primary */
            cursor: pointer;
            margin-top: -6px; /* You need to specify a margin in Chrome, but in Firefox and IE it is automatic */
            box-shadow: 0 0 10px rgba(118, 219, 143, 0.5);
        }
        input[type=range]::-webkit-slider-runnable-track {
            width: 100%;
            height: 4px;
            cursor: pointer;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 2px;
        }
        input[type=range]:focus {
            outline: none;
        }
        
        /* Modal Animation */
        @keyframes fadeIn {
            from { opacity: 0; backdrop-filter: blur(0px); }
            to { opacity: 1; backdrop-filter: blur(10px); }
        }
        @keyframes slideUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        .modal-overlay[data-state="open"] {
            animation: fadeIn 0.2s ease-out forwards;
        }
        .modal-content[data-state="open"] {
            animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
    </style>
</head>
<body class="bg-background text-on-background min-h-screen flex selection:bg-primary-container selection:text-on-primary-container">
<!-- TopNavBar (Mobile Only) -->
<header class="md:hidden bg-surface-container/40 dark:bg-surface-container/40 backdrop-blur-xl docked full-width top-0 border-b border-white/10 shadow-sm flex justify-between items-center px-container-padding w-full h-16 fixed z-40">
<div class="font-headline-md text-headline-md font-bold text-primary">
            Agro-Intelligence Oversight
        </div>
<div class="flex gap-4">
<button class="text-on-surface-variant hover:text-primary transition-colors cursor-pointer active:scale-95">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 0;">notifications</span>
</button>
<button class="text-primary hover:text-primary transition-colors cursor-pointer active:scale-95">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">settings</span>
</button>
</div>
</header>
<!-- SideNavBar (Desktop Only) -->
<nav class="hidden md:flex bg-surface-container-lowest dark:bg-surface-container-lowest h-screen w-20 hover:w-64 transition-all duration-300 ease-in-out fixed left-0 top-0 z-50 border-r border-white/5 shadow-2xl flex-col py-6 h-full group overflow-hidden">
<div class="flex flex-col items-center group-hover:items-start group-hover:px-6 w-full mb-8">
<div class="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center mb-4 group-hover:mb-2 shrink-0 border border-primary/30">
<span class="material-symbols-outlined text-primary" style="font-variation-settings: 'FILL' 1;">terminal</span>
</div>
<div class="hidden group-hover:block transition-opacity opacity-0 group-hover:opacity-100 duration-300">
<h1 class="font-headline-sm text-headline-sm text-primary-fixed truncate w-full">AUDIT_OS_V1</h1>
<p class="font-label-md text-label-md text-primary-fixed-dim/70 tracking-widest uppercase">Terminal Active</p>
</div>
</div>
<ul class="flex-1 w-full space-y-2">
<li>
<a class="flex items-center text-on-surface-variant hover:text-primary mx-2 p-3 hover:bg-surface-variant/20 rounded-lg transition-colors cursor-pointer active:scale-95" href="#">
<span class="material-symbols-outlined w-6 h-6 flex-shrink-0 flex items-center justify-center" data-icon="dashboard">dashboard</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider hidden group-hover:block whitespace-nowrap">Dashboard</span>
</a>
</li>
<li>
<a class="flex items-center text-on-surface-variant hover:text-primary mx-2 p-3 hover:bg-surface-variant/20 rounded-lg transition-colors cursor-pointer active:scale-95" href="#">
<span class="material-symbols-outlined w-6 h-6 flex-shrink-0 flex items-center justify-center" data-icon="security_update_warning">security_update_warning</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider hidden group-hover:block whitespace-nowrap">Risk Analysis</span>
</a>
</li>
<li>
<a class="flex items-center text-on-surface-variant hover:text-primary mx-2 p-3 hover:bg-surface-variant/20 rounded-lg transition-colors cursor-pointer active:scale-95" href="#">
<span class="material-symbols-outlined w-6 h-6 flex-shrink-0 flex items-center justify-center" data-icon="monitoring">monitoring</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider hidden group-hover:block whitespace-nowrap">Telemetry</span>
</a>
</li>
<li>
<a class="flex items-center text-on-surface-variant hover:text-primary mx-2 p-3 hover:bg-surface-variant/20 rounded-lg transition-colors cursor-pointer active:scale-95" href="#">
<span class="material-symbols-outlined w-6 h-6 flex-shrink-0 flex items-center justify-center" data-icon="fact_check">fact_check</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider hidden group-hover:block whitespace-nowrap">Audits</span>
</a>
</li>
<li>
<a class="flex items-center bg-primary-container text-on-primary-container rounded-lg mx-2 p-3 hover:bg-surface-variant/20 transition-colors cursor-pointer active:scale-95" href="#">
<span class="material-symbols-outlined w-6 h-6 flex-shrink-0 flex items-center justify-center" data-icon="settings" style="font-variation-settings: 'FILL' 1;">settings</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider hidden group-hover:block whitespace-nowrap">Settings</span>
</a>
</li>
</ul>
<div class="mt-auto w-full">
<div class="px-4 mb-4 hidden group-hover:block">
<button class="w-full bg-primary text-on-primary font-label-md text-label-md uppercase py-2 rounded-md hover:bg-primary-fixed-dim transition-colors shadow-sm">
                    Export Report
                </button>
</div>
<ul class="w-full space-y-2 border-t border-white/5 pt-4">
<li>
<a class="flex items-center text-on-surface-variant hover:text-primary mx-2 p-3 hover:bg-surface-variant/20 rounded-lg transition-colors cursor-pointer active:scale-95" href="#">
<span class="material-symbols-outlined w-6 h-6 flex-shrink-0 flex items-center justify-center" data-icon="help">help</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider hidden group-hover:block whitespace-nowrap">Support</span>
</a>
</li>
<li>
<a class="flex items-center text-on-surface-variant hover:text-primary mx-2 p-3 hover:bg-surface-variant/20 rounded-lg transition-colors cursor-pointer active:scale-95" href="#">
<span class="material-symbols-outlined w-6 h-6 flex-shrink-0 flex items-center justify-center" data-icon="logout">logout</span>
<span class="ml-4 font-label-md text-label-md uppercase tracking-wider hidden group-hover:block whitespace-nowrap">Logout</span>
</a>
</li>
</ul>
</div>
</nav>
<!-- Main Content Canvas -->
<main class="flex-1 md:ml-20 transition-all duration-300 pt-16 md:pt-0 p-container-padding flex flex-col gap-card-gap max-w-[1600px] mx-auto w-full">
<!-- Header -->
<header class="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 pb-4 border-b border-white/5">
<div>
<h1 class="font-display-lg text-display-lg text-primary-fixed mb-1">Model Configuration</h1>
<p class="font-body-lg text-body-lg text-on-surface-variant">Pipeline Management &amp; Hyperparameter Tuning</p>
</div>
<div class="flex gap-4">
<button class="px-6 py-2 rounded-DEFAULT glass-panel text-on-surface hover:text-primary transition-all font-label-md text-label-md uppercase tracking-wider flex items-center gap-2" id="btn-test">
<span class="material-symbols-outlined text-[18px]">hub</span>
                    Test Connection
                </button>
<button class="px-6 py-2 rounded-DEFAULT bg-primary text-on-primary hover:bg-primary-fixed-dim transition-all font-label-md text-label-md uppercase tracking-wider flex items-center gap-2 shadow-[0_0_15px_rgba(118,219,143,0.3)] hover:shadow-[0_0_20px_rgba(118,219,143,0.5)]" id="btn-apply">
<span class="material-symbols-outlined text-[18px]" style="font-variation-settings: 'FILL' 1;">save</span>
                    Apply Changes
                </button>
</div>
</header>
<!-- Bento Grid Layout -->
<div class="grid grid-cols-1 lg:grid-cols-12 gap-card-gap">
<!-- Predictor Section (Span 8) -->
<section class="lg:col-span-8 glass-panel rounded-xl p-6 flex flex-col gap-6 relative overflow-hidden">
<!-- Subtle background accent -->
<div class="absolute -top-24 -right-24 w-64 h-64 bg-primary/5 rounded-full blur-3xl pointer-events-none"></div>
<div class="flex justify-between items-start">
<div>
<h2 class="font-headline-md text-headline-md text-on-surface flex items-center gap-2">
<span class="material-symbols-outlined text-primary">online_prediction</span>
                            Active Predictor
                        </h2>
<p class="font-body-sm text-body-sm text-on-surface-variant mt-1">Core telemetry forecasting model</p>
</div>
<div class="relative group">
<select class="appearance-none bg-surface-container-high border border-outline-variant text-on-surface rounded-lg px-4 py-2 pr-10 font-body-md text-body-md focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-colors cursor-pointer">
<option selected="" value="xgboost">XGBoost v2.1</option>
<option value="lightgbm">LightGBM v3.3</option>
<option value="rf">Random Forest</option>
</select>
<span class="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-on-surface-variant pointer-events-none">expand_more</span>
</div>
</div>
<!-- Metrics Cards -->
<div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-2">
<div class="bg-surface-container-low/50 border border-white/5 rounded-lg p-4 flex flex-col">
<span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-2">Mean Absolute Error</span>
<div class="flex items-end gap-2">
<span class="font-headline-lg text-headline-lg text-primary data-value">0.024</span>
<span class="font-body-sm text-body-sm text-tertiary mb-1">↓ 0.002</span>
</div>
</div>
<div class="bg-surface-container-low/50 border border-white/5 rounded-lg p-4 flex flex-col">
<span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-2">Root Mean Sq. Error</span>
<div class="flex items-end gap-2">
<span class="font-headline-lg text-headline-lg text-on-surface data-value">0.038</span>
<span class="font-body-sm text-body-sm text-on-surface-variant mb-1">Steady</span>
</div>
</div>
<div class="bg-surface-container-low/50 border border-white/5 rounded-lg p-4 flex flex-col">
<span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-2">R² Score</span>
<div class="flex items-end gap-2">
<span class="font-headline-lg text-headline-lg text-primary-fixed data-value">0.942</span>
<span class="font-body-sm text-body-sm text-tertiary mb-1">↑ 0.01</span>
</div>
</div>
</div>
<!-- SHAP Explainability Settings inline -->
<div class="mt-auto pt-4 border-t border-white/5 flex items-center justify-between">
<div class="flex items-center gap-2 text-on-surface-variant">
<span class="material-symbols-outlined text-[18px]">analytics</span>
<span class="font-body-sm text-body-sm">SHAP Explainability View</span>
</div>
<div class="flex items-center gap-3">
<span class="font-label-md text-label-md uppercase text-on-surface-variant">Top Variables:</span>
<div class="flex bg-surface-container-high rounded-md p-1 border border-white/5">
<button class="px-3 py-1 rounded text-body-sm font-body-sm bg-surface-variant text-on-surface transition-colors">Top 5</button>
<button class="px-3 py-1 rounded text-body-sm font-body-sm text-on-surface-variant hover:text-on-surface transition-colors">Top 8</button>
</div>
</div>
</div>
</section>
<!-- RAG/LLM Config (Span 4) -->
<aside class="lg:col-span-4 glass-panel rounded-xl p-6 flex flex-col gap-6 relative">
<div class="flex items-center gap-2 mb-2">
<span class="material-symbols-outlined text-tertiary">memory</span>
<h2 class="font-headline-md text-headline-md text-on-surface">LLM Interrogator</h2>
</div>
<div class="space-y-5">
<!-- Provider -->
<div class="flex flex-col gap-2">
<label class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Provider Engine</label>
<div class="relative">
<select class="w-full appearance-none bg-surface-container-low border border-white/10 text-on-surface rounded-lg px-4 py-2 pr-10 font-body-md text-body-md focus:outline-none focus:border-tertiary focus:ring-1 focus:ring-tertiary transition-colors">
<option selected="" value="gpt4o">OpenAI GPT-4o</option>
<option value="claude3">Anthropic Claude 3.5</option>
<option value="llama3">Meta Llama 3 70B</option>
</select>
<span class="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-on-surface-variant pointer-events-none">expand_more</span>
</div>
</div>
<!-- Temperature -->
<div class="flex flex-col gap-2">
<div class="flex justify-between items-center">
<label class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Creativity (Temperature)</label>
<span class="font-mono-data text-mono-data text-tertiary data-value">0.1</span>
</div>
<input class="w-full accent-tertiary" max="1" min="0" step="0.1" style="--tw-accent: #89ceff;" type="range" value="0.1"/>
<div class="flex justify-between text-xs text-on-surface-variant/50">
<span>Precise</span>
<span>Creative</span>
</div>
</div>
<!-- Similarity Threshold -->
<div class="flex flex-col gap-2">
<div class="flex justify-between items-center">
<label class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Vector Similarity Cutoff</label>
<span class="font-mono-data text-mono-data text-tertiary data-value">0.75</span>
</div>
<input class="w-full accent-tertiary" max="1" min="0" step="0.05" style="--tw-accent: #89ceff;" type="range" value="0.75"/>
</div>
</div>
</aside>
<!-- Ensemble Settings (Span 12) -->
<section class="lg:col-span-12 glass-panel rounded-xl p-6 flex flex-col gap-6">
<header class="flex justify-between items-end border-b border-white/5 pb-4">
<div>
<h2 class="font-headline-md text-headline-md text-on-surface flex items-center gap-2">
<span class="material-symbols-outlined text-secondary">scatter_plot</span>
                            Anomaly Ensemble Weights
                        </h2>
<p class="font-body-sm text-body-sm text-on-surface-variant mt-1">Adjust contribution of distinct outlier detection algorithms.</p>
</div>
<div class="flex flex-col items-end gap-1 bg-surface-container-low/50 px-4 py-2 rounded-lg border border-error/20">
<span class="font-label-md text-label-md text-error uppercase tracking-wider">Global Threshold</span>
<div class="flex items-center gap-2">
<span class="font-headline-sm text-headline-sm text-error">0.65</span>
<span class="material-symbols-outlined text-error text-[16px]">warning</span>
</div>
</div>
</header>
<div class="grid grid-cols-1 md:grid-cols-3 gap-8">
<!-- Isolation Forest -->
<div class="flex flex-col gap-3 group">
<div class="flex justify-between items-center">
<div class="flex items-center gap-2">
<div class="w-2 h-2 rounded-full bg-secondary"></div>
<label class="font-body-md text-body-md text-on-surface font-medium">Isolation Forest</label>
</div>
<span class="font-mono-data text-mono-data text-secondary bg-secondary/10 px-2 py-0.5 rounded">w: 0.45</span>
</div>
<input class="w-full group-hover:opacity-100 opacity-80 transition-opacity" max="1" min="0" step="0.05" type="range" value="0.45"/>
</div>
<!-- Local Outlier Factor -->
<div class="flex flex-col gap-3 group">
<div class="flex justify-between items-center">
<div class="flex items-center gap-2">
<div class="w-2 h-2 rounded-full bg-tertiary"></div>
<label class="font-body-md text-body-md text-on-surface font-medium">LOF (Density)</label>
</div>
<span class="font-mono-data text-mono-data text-tertiary bg-tertiary/10 px-2 py-0.5 rounded">w: 0.30</span>
</div>
<input class="w-full group-hover:opacity-100 opacity-80 transition-opacity" max="1" min="0" step="0.05" type="range" value="0.30"/>
</div>
<!-- ECOD -->
<div class="flex flex-col gap-3 group">
<div class="flex justify-between items-center">
<div class="flex items-center gap-2">
<div class="w-2 h-2 rounded-full bg-primary-fixed"></div>
<label class="font-body-md text-body-md text-on-surface font-medium">ECOD (Empirical)</label>
</div>
<span class="font-mono-data text-mono-data text-primary-fixed bg-primary-fixed/10 px-2 py-0.5 rounded">w: 0.25</span>
</div>
<input class="w-full group-hover:opacity-100 opacity-80 transition-opacity" max="1" min="0" step="0.05" type="range" value="0.25"/>
</div>
</div>
<!-- Summation indicator -->
<div class="w-full h-1 bg-surface-container-high rounded-full overflow-hidden flex mt-2">
<div class="h-full bg-secondary" style="width: 45%;"></div>
<div class="h-full bg-tertiary" style="width: 30%;"></div>
<div class="h-full bg-primary-fixed" style="width: 25%;"></div>
</div>
<div class="text-right font-label-md text-label-md text-on-surface-variant">Σ 1.00</div>
</section>
</div>
</main>
<!-- Modals -->
<!-- Test Connection Modal -->
<div class="fixed inset-0 z-[100] hidden items-center justify-center p-4" id="modal-test">
<div class="absolute inset-0 bg-background/80 backdrop-blur-sm modal-overlay" id="overlay-test"></div>
<div class="relative bg-surface-container-low border border-white/10 rounded-xl shadow-2xl w-full max-w-md overflow-hidden modal-content flex flex-col">
<!-- Pulsing line at top -->
<div class="h-1 w-full bg-gradient-to-r from-transparent via-tertiary to-transparent opacity-50 relative overflow-hidden">
<div class="absolute inset-0 bg-tertiary w-1/3 animate-[translateX_1.5s_infinite_ease-in-out]" style="animation: pulse-line 1.5s infinite;"></div>
</div>
<div class="p-6">
<div class="flex items-center gap-4 mb-4">
<div class="w-12 h-12 rounded-full bg-tertiary/10 flex items-center justify-center border border-tertiary/30">
<span class="material-symbols-outlined text-tertiary text-2xl animate-spin" style="animation-duration: 3s;">hub</span>
</div>
<div>
<h3 class="font-headline-sm text-headline-sm text-on-surface">Verifying Connection</h3>
<p class="font-body-sm text-body-sm text-on-surface-variant">Pinging model endpoints...</p>
</div>
</div>
<div class="space-y-3 font-mono-data text-mono-data text-xs text-on-surface-variant bg-surface-container-lowest p-4 rounded-lg border border-white/5">
<div class="flex justify-between"><span>&gt; Ping ML_Cluster_Alpha</span><span class="text-primary">OK (12ms)</span></div>
<div class="flex justify-between"><span>&gt; Check OpenAI API Key</span><span class="text-primary">Valid</span></div>
<div class="flex justify-between"><span>&gt; Verify Vector DB Sync</span><span class="text-tertiary animate-pulse">Syncing...</span></div>
</div>
</div>
<div class="px-6 py-4 border-t border-white/5 flex justify-end">
<button class="btn-close-modal px-4 py-2 rounded text-on-surface font-label-md text-label-md hover:bg-surface-variant/50 transition-colors">Cancel</button>
</div>
</div>
</div>
<!-- Apply Changes Modal -->
<div class="fixed inset-0 z-[100] hidden items-center justify-center p-4" id="modal-apply">
<div class="absolute inset-0 bg-background/80 backdrop-blur-sm modal-overlay" id="overlay-apply"></div>
<div class="relative bg-surface-container-low border border-primary/20 rounded-xl shadow-[0_0_40px_rgba(61,163,93,0.1)] w-full max-w-md overflow-hidden modal-content flex flex-col">
<div class="p-6">
<div class="flex items-start gap-4 mb-6">
<div class="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center border border-primary/30 shrink-0">
<span class="material-symbols-outlined text-primary text-2xl">warning</span>
</div>
<div>
<h3 class="font-headline-sm text-headline-sm text-on-surface mb-2">Deploy Configuration?</h3>
<p class="font-body-sm text-body-sm text-on-surface-variant">This will hot-swap the active ensemble weights and hyper-parameters in the live environment. Temporary telemetry latency (&lt; 2s) may occur.</p>
</div>
</div>
<div class="bg-surface-container-lowest p-4 rounded-lg border border-white/5 flex flex-col gap-2 mb-6">
<span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider border-b border-white/5 pb-2">Diff Summary</span>
<div class="flex justify-between text-body-sm"><span class="text-on-surface-variant">Active Model</span> <span class="text-on-surface">XGBoost v2.1</span></div>
<div class="flex justify-between text-body-sm"><span class="text-on-surface-variant">Ensemble LOF</span> <span class="text-primary">0.25 → 0.30</span></div>
<div class="flex justify-between text-body-sm"><span class="text-on-surface-variant">LLM Temp</span> <span class="text-on-surface">0.1 (Unchanged)</span></div>
</div>
<div class="flex gap-3 w-full">
<button class="btn-close-modal flex-1 px-4 py-3 rounded-lg border border-outline-variant text-on-surface font-label-md text-label-md hover:bg-surface-variant/50 transition-colors uppercase">Cancel</button>
<button class="btn-close-modal flex-1 px-4 py-3 rounded-lg bg-primary text-on-primary font-label-md text-label-md hover:bg-primary-fixed-dim transition-colors uppercase shadow-[0_0_15px_rgba(118,219,143,0.3)]">Confirm Deploy</button>
</div>
</div>
</div>
</div>
<style>
        @keyframes pulse-line {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(300%); }
        }
    </style>
<script>
        // Simple Modal Logic
        const btnTest = document.getElementById('btn-test');
        const modalTest = document.getElementById('modal-test');
        const overlayTest = document.getElementById('overlay-test');

        const btnApply = document.getElementById('btn-apply');
        const modalApply = document.getElementById('modal-apply');
        const overlayApply = document.getElementById('overlay-apply');

        const closeBtns = document.querySelectorAll('.btn-close-modal');

        function openModal(modal, overlay) {
            modal.classList.remove('hidden');
            modal.classList.add('flex');
            // Trigger reflow
            void modal.offsetWidth;
            overlay.setAttribute('data-state', 'open');
            modal.querySelector('.modal-content').setAttribute('data-state', 'open');
        }

        function closeModal(modal, overlay) {
             overlay.removeAttribute('data-state');
             modal.querySelector('.modal-content').removeAttribute('data-state');
             
             // Wait for animation to finish
             setTimeout(() => {
                 modal.classList.add('hidden');
                 modal.classList.remove('flex');
             }, 200); // match animation duration
        }

        btnTest.addEventListener('click', () => openModal(modalTest, overlayTest));
        btnApply.addEventListener('click', () => openModal(modalApply, overlayApply));

        closeBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const modal = e.target.closest('.fixed');
                const overlay = modal.querySelector('.modal-overlay');
                closeModal(modal, overlay);
            });
        });

        // Update range values visually (simple implementation)
        document.querySelectorAll('input[type="range"]').forEach(input => {
            input.addEventListener('input', (e) => {
                const targetDisplay = e.target.parentElement.querySelector('.data-value') || 
                                      e.target.parentElement.querySelector('.text-mono-data.px-2');
                if(targetDisplay) {
                    if(targetDisplay.textContent.includes('w:')) {
                         targetDisplay.textContent = `w: ${parseFloat(e.target.value).toFixed(2)}`;
                    } else {
                         targetDisplay.textContent = parseFloat(e.target.value).toFixed(2);
                    }
                }
            });
        });
    </script>
</body></html>

<!-- Integrity & Fairness Monitor -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Integrity and Fairness Monitor | Agro-Intelligence Oversight</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Outfit:wght@400;600;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    colors: {
                        "outline-variant": "#3f4a3f",
                        "surface-container-low": "#171d17",
                        "primary-container": "#3da35d",
                        "surface-container-lowest": "#0a100a",
                        "on-secondary-fixed-variant": "#1e502e",
                        "inverse-on-surface": "#2c322b",
                        "surface-container": "#1b211b",
                        "surface-variant": "#30362f",
                        "surface-container-highest": "#30362f",
                        "inverse-primary": "#006d33",
                        "primary-fixed": "#92f8a9",
                        "on-surface-variant": "#becabc",
                        "tertiary-fixed-dim": "#89ceff",
                        "on-surface": "#dee4da",
                        "surface-tint": "#76db8f",
                        "tertiary-fixed": "#c9e6ff",
                        "on-error-container": "#ffdad6",
                        "on-tertiary-fixed": "#001e2f",
                        "on-background": "#dee4da",
                        "on-tertiary-fixed-variant": "#004c6e",
                        "error-container": "#93000a",
                        "secondary-container": "#205331",
                        "primary-fixed-dim": "#76db8f",
                        "on-secondary-container": "#8fc599",
                        "on-primary-container": "#003114",
                        "tertiary": "#89ceff",
                        "surface-bright": "#343b34",
                        "secondary": "#9dd3a7",
                        "on-primary-fixed": "#00210b",
                        "on-tertiary": "#00344d",
                        "on-primary": "#003918",
                        "secondary-fixed": "#b8f0c2",
                        "background": "#0f150f",
                        "outline": "#889487",
                        "tertiary-container": "#009ada",
                        "primary": "#76db8f",
                        "on-tertiary-container": "#002d43",
                        "surface-container-high": "#252c25",
                        "surface-dim": "#0f150f",
                        "on-error": "#690005",
                        "inverse-surface": "#dee4da",
                        "surface": "#0f150f",
                        "on-secondary-fixed": "#00210c",
                        "on-primary-fixed-variant": "#005225",
                        "on-secondary": "#01391a",
                        "secondary-fixed-dim": "#9dd3a7",
                        "error": "#ffb4ab"
                    },
                    borderRadius: {
                        "DEFAULT": "0.125rem",
                        "lg": "0.25rem",
                        "xl": "0.5rem",
                        "full": "0.75rem"
                    },
                    spacing: {
                        "gutter": "16px",
                        "card-gap": "20px",
                        "container-padding": "24px",
                        "unit": "4px"
                    },
                    fontFamily: {
                        "body-md": ["Inter", "sans-serif"],
                        "headline-sm": ["Outfit", "sans-serif"],
                        "body-sm": ["Inter", "sans-serif"],
                        "headline-md": ["Outfit", "sans-serif"],
                        "display-lg": ["Outfit", "sans-serif"],
                        "headline-lg": ["Outfit", "sans-serif"],
                        "mono-data": ["monospace"],
                        "label-md": ["Inter", "sans-serif"],
                        "body-lg": ["Inter", "sans-serif"]
                    },
                    fontSize: {
                        "body-md": ["16px", { "lineHeight": "24px", "fontWeight": "400" }],
                        "headline-sm": ["20px", { "lineHeight": "28px", "fontWeight": "600" }],
                        "body-sm": ["14px", { "lineHeight": "20px", "fontWeight": "400" }],
                        "headline-md": ["24px", { "lineHeight": "32px", "fontWeight": "600" }],
                        "display-lg": ["48px", { "lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "700" }],
                        "headline-lg": ["32px", { "lineHeight": "40px", "fontWeight": "600" }],
                        "mono-data": ["14px", { "lineHeight": "20px", "fontWeight": "500" }],
                        "label-md": ["12px", { "lineHeight": "16px", "letterSpacing": "0.05em", "fontWeight": "600" }],
                        "body-lg": ["18px", { "lineHeight": "28px", "fontWeight": "400" }]
                    }
                }
            }
        }
    </script>
<style>
        body {
            background-color: #0f150f;
            color: #dee4da;
            overflow-x: hidden;
        }
        
        .glass-panel {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .glass-modal {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(40px);
            -webkit-backdrop-filter: blur(40px);
            box-shadow: 0 0 30px rgba(61, 163, 93, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.15);
        }

        .pulse-alert {
            animation: pulseBorder 2s infinite;
        }

        @keyframes pulseBorder {
            0% { border-color: rgba(255, 180, 171, 0.5); box-shadow: 0 0 0 0 rgba(255, 180, 171, 0.4); }
            70% { border-color: rgba(255, 180, 171, 1); box-shadow: 0 0 0 6px rgba(255, 180, 171, 0); }
            100% { border-color: rgba(255, 180, 171, 0.5); box-shadow: 0 0 0 0 rgba(255, 180, 171, 0); }
        }

        .chart-grid {
            background-image: linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px);
            background-size: 20px 20px;
        }

        /* Tooltip Setup */
        .has-tooltip { position: relative; cursor: help; }
        .tooltip-content {
            visibility: hidden;
            opacity: 0;
            transition: opacity 0.2s, visibility 0.2s;
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%) translateY(-8px);
            width: max-content;
            max-width: 250px;
            z-index: 100;
        }
        .has-tooltip:hover .tooltip-content {
            visibility: visible;
            opacity: 1;
        }
        
        /* Custom Scrollbar for data tables */
        .custom-scrollbar::-webkit-scrollbar { height: 6px; width: 6px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: rgba(255,255,255,0.02); }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(118, 219, 143, 0.3); border-radius: 4px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(118, 219, 143, 0.6); }
    </style>
</head>
<body class="font-body-md text-on-surface bg-background antialiased flex h-screen overflow-hidden">
<!-- SideNavBar -->
<nav class="bg-surface-container-lowest dark:bg-surface-container-lowest text-primary font-label-md text-label-md uppercase tracking-wider h-screen w-20 hover:w-64 transition-all duration-300 ease-in-out fixed left-0 top-0 z-50 border-r border-white/5 shadow-2xl group flex flex-col py-6 h-full hidden md:flex">
<!-- Header -->
<div class="px-container-padding mb-8 flex items-center overflow-hidden whitespace-nowrap">
<span class="material-symbols-outlined text-[32px] mr-4 text-primary-fixed" style="font-variation-settings: 'FILL' 1;">terminal</span>
<div class="flex flex-col opacity-0 group-hover:opacity-100 transition-opacity duration-300">
<span class="font-headline-sm text-headline-sm text-primary-fixed normal-case">AUDIT_OS_V1</span>
<span class="text-[10px] text-primary opacity-70">Terminal Active</span>
</div>
</div>
<!-- Navigation Links -->
<div class="flex-1 overflow-y-auto overflow-x-hidden space-y-2">
<a class="flex items-center text-on-surface-variant hover:text-primary mx-2 px-4 py-3 rounded-lg hover:bg-surface-variant/20 transition-all duration-300" href="#">
<span class="material-symbols-outlined min-w-[24px]">dashboard</span>
<span class="ml-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Dashboard</span>
</a>
<a class="flex items-center text-on-surface-variant hover:text-primary mx-2 px-4 py-3 rounded-lg hover:bg-surface-variant/20 transition-all duration-300" href="#">
<span class="material-symbols-outlined min-w-[24px]">security_update_warning</span>
<span class="ml-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Risk Analysis</span>
</a>
<a class="flex items-center text-on-surface-variant hover:text-primary mx-2 px-4 py-3 rounded-lg hover:bg-surface-variant/20 transition-all duration-300" href="#">
<span class="material-symbols-outlined min-w-[24px]">monitoring</span>
<span class="ml-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Telemetry</span>
</a>
<!-- Active State Context: Integrity and Fairness Monitor logically falls under Audits or Risk Analysis. Picking Audits. -->
<a class="flex items-center bg-primary-container text-on-primary-container rounded-lg mx-2 px-4 py-3 transition-all duration-300" href="#">
<span class="material-symbols-outlined min-w-[24px]" style="font-variation-settings: 'FILL' 1;">fact_check</span>
<span class="ml-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap font-bold">Audits</span>
</a>
<a class="flex items-center text-on-surface-variant hover:text-primary mx-2 px-4 py-3 rounded-lg hover:bg-surface-variant/20 transition-all duration-300" href="#">
<span class="material-symbols-outlined min-w-[24px]">settings</span>
<span class="ml-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Settings</span>
</a>
</div>
<!-- Footer Actions -->
<div class="mt-auto px-2 space-y-2">
<button class="w-full flex items-center bg-surface-variant/20 text-primary mx-2 px-4 py-3 rounded-lg hover:bg-surface-variant/40 transition-all duration-300 border border-primary/20 hover:border-primary/50 group/btn overflow-hidden">
<span class="material-symbols-outlined min-w-[24px]">download</span>
<span class="ml-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Export Report</span>
</button>
<a class="flex items-center text-on-surface-variant hover:text-primary px-4 py-2 rounded-lg hover:bg-surface-variant/20 transition-all duration-300" href="#">
<span class="material-symbols-outlined min-w-[24px]">help</span>
<span class="ml-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Support</span>
</a>
<a class="flex items-center text-on-surface-variant hover:text-primary px-4 py-2 rounded-lg hover:bg-surface-variant/20 transition-all duration-300" href="#">
<span class="material-symbols-outlined min-w-[24px]">logout</span>
<span class="ml-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Logout</span>
</a>
</div>
</nav>
<!-- Main Content Canvas -->
<main class="flex-1 flex flex-col md:ml-20 h-screen overflow-hidden bg-background">
<!-- TopNavBar (Mobile mainly, but provides header context here per instructions to use it) -->
<header class="bg-surface-container/40 dark:bg-surface-container/40 backdrop-blur-xl text-primary font-body-md text-body-md docked full-width top-0 border-b border-white/10 shadow-sm flex justify-between items-center px-container-padding w-full h-16 z-40 relative">
<div class="flex items-center gap-4">
<div class="md:hidden">
<span class="material-symbols-outlined font-headline-md text-headline-md font-bold text-primary cursor-pointer active:scale-95">menu</span>
</div>
<h1 class="font-headline-md text-headline-md font-bold text-primary tracking-tight">Agro-Intelligence Oversight</h1>
</div>
<!-- Top Nav Links (Hidden on mobile) -->
<div class="hidden md:flex items-center gap-8 h-full">
<a class="text-on-surface-variant hover:text-primary transition-colors cursor-pointer active:scale-95 h-full flex items-center px-2" href="#">Telemetry</a>
<a class="text-primary border-b-2 border-primary pb-1 hover:text-primary transition-colors cursor-pointer active:scale-95 h-full flex items-center px-2 pt-1 font-medium" href="#">Audits</a>
<a class="text-on-surface-variant hover:text-primary transition-colors cursor-pointer active:scale-95 h-full flex items-center px-2" href="#">Inventory</a>
</div>
<div class="flex items-center gap-4">
<button class="text-on-surface-variant hover:text-primary transition-colors cursor-pointer active:scale-95 relative">
<span class="material-symbols-outlined">notifications</span>
<span class="absolute top-0 right-0 w-2 h-2 bg-error rounded-full animate-pulse"></span>
</button>
<button class="text-on-surface-variant hover:text-primary transition-colors cursor-pointer active:scale-95">
<span class="material-symbols-outlined">settings</span>
</button>
<div class="w-8 h-8 rounded-full bg-surface-variant overflow-hidden ml-2 border border-white/10">
<img alt="Auditor Profile" class="w-full h-full object-cover" data-alt="A highly detailed, professional headshot of a stern systems auditor wearing augmented reality glasses, lit by cool green monitor glows in a dark tech environment. High contrast, cinematic lighting, emphasizing cybernetic precision and vigilant oversight." src="https://lh3.googleusercontent.com/aida-public/AB6AXuAoECHdFsRm0K8wKpkzcipcYv8zZt9nLzDc2jqqnefPzGlcP10ir6SgVA2I75uL4i_trZqaoSGENE6oCcRzK4MptAFF2eOXv_Td2DblJvBy3MKTyRTFRoYH0LYneE0csFx4hn5xmwgVD9pMXqDuY-hw6zICd_2YlUgDvO4LhxaV5KCMN8RztQQIvA938tclZ6_KFtGbIav-9t552jbxMuiybXnvx9C11L_kvoFTnXUGAO82inc6e-uQ26XInzZzpIRn_UQ9m-FC540"/>
</div>
</div>
</header>
<!-- Scrollable Dashboard Content -->
<div class="flex-1 overflow-y-auto custom-scrollbar p-container-padding space-y-card-gap">
<!-- Page Header -->
<div class="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-2">
<div>
<div class="flex items-center gap-2 mb-1">
<span class="material-symbols-outlined text-primary text-sm">gavel</span>
<span class="font-label-md text-label-md text-primary uppercase tracking-widest">Compliance Matrix</span>
</div>
<h2 class="font-headline-lg text-headline-lg text-on-surface">Integrity &amp; Fairness Monitor</h2>
<p class="font-body-sm text-body-sm text-on-surface-variant mt-1 max-w-2xl">Real-time analysis of auditing algorithm bias, disparate impact metrics, and demographic parity across export segments.</p>
</div>
<div class="flex items-center gap-3">
<div class="glass-panel px-4 py-2 rounded-lg flex items-center gap-2">
<span class="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
<span class="font-mono-data text-mono-data text-primary">SYS_NOMINAL</span>
</div>
<button class="glass-panel hover:bg-white/5 px-4 py-2 rounded-lg flex items-center gap-2 transition-colors border border-outline/30">
<span class="material-symbols-outlined text-sm">filter_list</span>
<span class="font-label-md text-label-md">FILTER</span>
</button>
</div>
</div>
<!-- Bento Grid Layout -->
<div class="grid grid-cols-1 md:grid-cols-12 gap-card-gap">
<!-- Alerts Panel (High Priority) -->
<div class="md:col-span-12 xl:col-span-4 flex flex-col gap-card-gap">
<div class="glass-modal rounded-xl p-6 flex-1 relative overflow-hidden pulse-alert border-error/50">
<!-- Abstract hazard background -->
<div class="absolute -right-10 -top-10 w-40 h-40 bg-error/10 rounded-full blur-3xl pointer-events-none"></div>
<div class="flex items-center justify-between mb-6">
<h3 class="font-headline-sm text-headline-sm text-error flex items-center gap-2">
<span class="material-symbols-outlined">warning</span>
                                Significant Disparity Detected
                            </h3>
<span class="font-label-md text-label-md text-error bg-error/10 px-2 py-1 rounded">SEV_1</span>
</div>
<div class="space-y-4">
<!-- Alert Item 1 -->
<div class="bg-surface-container-high/50 border border-error/20 p-4 rounded-lg relative overflow-hidden">
<div class="absolute left-0 top-0 bottom-0 w-1 bg-error"></div>
<div class="flex justify-between items-start mb-2">
<span class="font-label-md text-label-md text-on-surface">False Positive Rate (FPR) Skew</span>
<span class="font-mono-data text-mono-data text-error">+14.2%</span>
</div>
<p class="font-body-sm text-body-sm text-on-surface-variant">Model flagging <strong>Palta</strong> shipments from Small Exporters at a disproportionate rate compared to Large Exporters.</p>
<div class="mt-3 flex gap-2">
<button class="text-[10px] uppercase tracking-wider bg-error/10 text-error px-2 py-1 rounded hover:bg-error/20 transition-colors">Investigate</button>
<button class="text-[10px] uppercase tracking-wider bg-surface-variant text-on-surface-variant px-2 py-1 rounded hover:bg-surface-bright transition-colors">Acknowledge</button>
</div>
</div>
<!-- Alert Item 2 -->
<div class="bg-surface-container-high/50 border border-outline/20 p-4 rounded-lg relative overflow-hidden">
<div class="absolute left-0 top-0 bottom-0 w-1 bg-tertiary"></div>
<div class="flex justify-between items-start mb-2">
<span class="font-label-md text-label-md text-on-surface">Selection Rate Variance</span>
<span class="font-mono-data text-mono-data text-tertiary">Watch</span>
</div>
<p class="font-body-sm text-body-sm text-on-surface-variant">Disparate Impact Ratio for <strong>Uva</strong> approaching threshold (0.82). Monitor next 48h.</p>
</div>
</div>
</div>
</div>
<!-- Metrics Grid -->
<div class="md:col-span-12 xl:col-span-8 grid grid-cols-1 md:grid-cols-2 gap-card-gap">
<!-- KPI 1 -->
<div class="glass-panel rounded-xl p-6 relative overflow-hidden group">
<div class="absolute bottom-0 left-0 w-full h-1/2 bg-gradient-to-t from-primary/10 to-transparent opacity-50"></div>
<div class="flex justify-between items-start relative z-10">
<div>
<div class="flex items-center gap-2 mb-2">
<span class="font-label-md text-label-md text-on-surface-variant uppercase">Global Disparate Impact</span>
<div class="has-tooltip">
<span class="material-symbols-outlined text-[16px] text-outline hover:text-primary transition-colors">info</span>
<div class="tooltip-content glass-modal p-3 rounded text-body-sm font-body-sm text-on-surface w-64 shadow-xl">
<strong>Disparate Impact Ratio (DIR)</strong><br/>
<span class="text-on-surface-variant text-xs mt-1 block">Ratio of selection rates for unprivileged vs privileged groups. A value &lt; 0.8 indicates adverse impact per 4/5ths rule.</span>
</div>
</div>
</div>
<div class="font-display-lg text-display-lg text-primary">0.94</div>
</div>
<div class="glass-panel p-2 rounded flex flex-col items-center justify-center">
<span class="material-symbols-outlined text-primary mb-1">balance</span>
<span class="font-mono-data text-[10px] text-primary">FAIR</span>
</div>
</div>
<!-- Mini sparkline mock -->
<div class="h-8 mt-4 flex items-end gap-1 opacity-60">
<div class="w-full bg-primary/20 h-[60%] rounded-t-sm"></div>
<div class="w-full bg-primary/40 h-[70%] rounded-t-sm"></div>
<div class="w-full bg-primary/30 h-[65%] rounded-t-sm"></div>
<div class="w-full bg-primary/60 h-[80%] rounded-t-sm"></div>
<div class="w-full bg-primary/80 h-[90%] rounded-t-sm"></div>
<div class="w-full bg-primary h-[94%] rounded-t-sm relative">
<div class="absolute -top-1 left-1/2 w-1.5 h-1.5 bg-white rounded-full transform -translate-x-1/2 shadow-[0_0_5px_#fff]"></div>
</div>
</div>
</div>
<!-- KPI 2 -->
<div class="glass-panel rounded-xl p-6 relative overflow-hidden group">
<div class="flex justify-between items-start relative z-10">
<div>
<div class="flex items-center gap-2 mb-2">
<span class="font-label-md text-label-md text-on-surface-variant uppercase">Equal Opportunity Diff</span>
<div class="has-tooltip">
<span class="material-symbols-outlined text-[16px] text-outline hover:text-primary transition-colors">info</span>
<div class="tooltip-content glass-modal p-3 rounded text-body-sm font-body-sm text-on-surface w-64 shadow-xl">
<strong>Equal Opportunity Difference</strong><br/>
<span class="text-on-surface-variant text-xs mt-1 block">Difference in True Positive Rates between groups. Ideal value is 0. Identifies if the model misses true anomalies in specific groups.</span>
</div>
</div>
</div>
<div class="font-display-lg text-display-lg text-on-surface flex items-baseline gap-1">
                                    -0.03 <span class="text-sm font-mono-data text-outline">Δ</span>
</div>
</div>
<div class="glass-panel p-2 rounded flex flex-col items-center justify-center">
<span class="material-symbols-outlined text-tertiary mb-1">analytics</span>
<span class="font-mono-data text-[10px] text-tertiary">STABLE</span>
</div>
</div>
<div class="mt-4 pt-4 border-t border-white/5 flex justify-between font-mono-data text-[11px]">
<span class="text-on-surface-variant">Target: ±0.05</span>
<span class="text-primary">Within Bounds</span>
</div>
</div>
<!-- Chart 1: FPR Parity -->
<div class="glass-panel rounded-xl p-6 md:col-span-2 flex flex-col">
<div class="flex justify-between items-center mb-6">
<div>
<h3 class="font-headline-sm text-headline-sm text-on-surface">FPR Parity: Product Segment</h3>
<p class="font-body-sm text-body-sm text-on-surface-variant">False Positive Rate comparison across primary export categories</p>
</div>
<div class="flex gap-2">
<span class="flex items-center gap-1 font-label-md text-[10px] text-on-surface-variant"><div class="w-2 h-2 rounded bg-primary"></div> Threshold</span>
<span class="flex items-center gap-1 font-label-md text-[10px] text-on-surface-variant"><div class="w-2 h-2 rounded bg-error"></div> Actual</span>
</div>
</div>
<!-- Custom CSS Bar Chart -->
<div class="flex-1 chart-grid relative pt-4 pb-6 min-h-[160px] flex items-end justify-around gap-4">
<!-- Y Axis Labels -->
<div class="absolute left-0 top-0 h-full flex flex-col justify-between font-mono-data text-[10px] text-outline pb-6">
<span>0.15</span>
<span>0.10</span>
<span>0.05</span>
<span>0.00</span>
</div>
<!-- Bars -->
<div class="w-full flex justify-around pl-8 h-full items-end z-10 relative">
<!-- Target Line Overlay -->
<div class="absolute w-full h-[1px] bg-primary/50 top-[33%] border-t border-dashed border-primary z-0"></div>
<!-- Palta -->
<div class="w-16 h-full flex items-end justify-center group relative cursor-pointer">
<div class="w-12 bg-error/80 h-[85%] rounded-t shadow-[0_0_15px_rgba(255,180,171,0.2)] border-t border-error transition-all group-hover:bg-error"></div>
<span class="absolute -bottom-6 font-mono-data text-[11px] text-on-surface">PALTA</span>
<!-- Tooltip -->
<div class="absolute -top-10 opacity-0 group-hover:opacity-100 transition-opacity glass-modal px-2 py-1 rounded text-xs font-mono-data text-error whitespace-nowrap z-20 pointer-events-none">FPR: 0.128 (!)</div>
</div>
<!-- Uva -->
<div class="w-16 h-full flex items-end justify-center group relative cursor-pointer">
<div class="w-12 bg-secondary/80 h-[40%] rounded-t border-t border-secondary transition-all group-hover:bg-secondary"></div>
<span class="absolute -bottom-6 font-mono-data text-[11px] text-on-surface">UVA</span>
<div class="absolute -top-10 opacity-0 group-hover:opacity-100 transition-opacity glass-modal px-2 py-1 rounded text-xs font-mono-data text-secondary whitespace-nowrap z-20 pointer-events-none">FPR: 0.060</div>
</div>
<!-- Arándano -->
<div class="w-16 h-full flex items-end justify-center group relative cursor-pointer">
<div class="w-12 bg-secondary/80 h-[35%] rounded-t border-t border-secondary transition-all group-hover:bg-secondary"></div>
<span class="absolute -bottom-6 font-mono-data text-[11px] text-on-surface">ARÁNDANO</span>
<div class="absolute -top-10 opacity-0 group-hover:opacity-100 transition-opacity glass-modal px-2 py-1 rounded text-xs font-mono-data text-secondary whitespace-nowrap z-20 pointer-events-none">FPR: 0.052</div>
</div>
</div>
</div>
</div>
</div>
<!-- Secondary Charts Row -->
<div class="md:col-span-12 grid grid-cols-1 lg:grid-cols-2 gap-card-gap">
<!-- Chart 2: Recall per Export Group -->
<div class="glass-panel rounded-xl p-6 flex flex-col h-[300px]">
<h3 class="font-headline-sm text-headline-sm text-on-surface mb-1">Recall per Export Group</h3>
<p class="font-body-sm text-body-sm text-on-surface-variant mb-4">True Positive Rate by exporter size category</p>
<div class="flex-1 flex flex-col justify-center space-y-4">
<!-- Small -->
<div class="space-y-1">
<div class="flex justify-between font-mono-data text-xs">
<span class="text-on-surface">Small Exporters (&lt;500k)</span>
<span class="text-tertiary">0.82</span>
</div>
<div class="h-2 w-full bg-surface-container-high rounded-full overflow-hidden">
<div class="h-full bg-tertiary/80 rounded-full" style="width: 82%"></div>
</div>
</div>
<!-- Medium -->
<div class="space-y-1">
<div class="flex justify-between font-mono-data text-xs">
<span class="text-on-surface">Medium Exporters (500k-5M)</span>
<span class="text-primary">0.91</span>
</div>
<div class="h-2 w-full bg-surface-container-high rounded-full overflow-hidden">
<div class="h-full bg-primary/80 rounded-full" style="width: 91%"></div>
</div>
</div>
<!-- Large -->
<div class="space-y-1">
<div class="flex justify-between font-mono-data text-xs">
<span class="text-on-surface">Large Exporters (&gt;5M)</span>
<span class="text-primary">0.94</span>
</div>
<div class="h-2 w-full bg-surface-container-high rounded-full overflow-hidden">
<div class="h-full bg-primary/80 rounded-full" style="width: 94%"></div>
</div>
</div>
</div>
</div>
<!-- Data Table / Heatmap hybrid for F1-Score by Port -->
<div class="glass-panel rounded-xl flex flex-col h-[300px] overflow-hidden">
<div class="p-6 pb-2">
<h3 class="font-headline-sm text-headline-sm text-on-surface">F1-Score by Destination Port</h3>
<p class="font-body-sm text-body-sm text-on-surface-variant">Harmonic mean of precision and recall per logistics node</p>
</div>
<div class="flex-1 overflow-auto custom-scrollbar">
<table class="w-full text-left border-collapse">
<thead class="bg-surface-container-high/50 border-b border-primary/30 sticky top-0 z-10">
<tr>
<th class="p-3 pl-6 font-label-md text-label-md text-on-surface-variant uppercase">Port Node</th>
<th class="p-3 font-label-md text-label-md text-on-surface-variant uppercase">Vol (TEU)</th>
<th class="p-3 pr-6 font-label-md text-label-md text-on-surface-variant uppercase text-right">F1-Score</th>
</tr>
</thead>
<tbody class="font-mono-data text-[13px] divide-y divide-white/5">
<tr class="hover:bg-white/5 transition-colors bg-white/[0.02]">
<td class="p-3 pl-6 text-on-surface flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-primary"></span> Rotterdam (NLD)</td>
<td class="p-3 text-on-surface-variant">14,250</td>
<td class="p-3 pr-6 text-right text-primary">0.96</td>
</tr>
<tr class="hover:bg-white/5 transition-colors">
<td class="p-3 pl-6 text-on-surface flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-primary"></span> Philadelphia (USA)</td>
<td class="p-3 text-on-surface-variant">11,800</td>
<td class="p-3 pr-6 text-right text-primary">0.93</td>
</tr>
<tr class="hover:bg-white/5 transition-colors bg-white/[0.02]">
<td class="p-3 pl-6 text-on-surface flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-tertiary"></span> Shanghai (CHN)</td>
<td class="p-3 text-on-surface-variant">8,420</td>
<td class="p-3 pr-6 text-right text-tertiary">0.88</td>
</tr>
<tr class="hover:bg-white/5 transition-colors border-l-2 border-error">
<td class="p-3 pl-5 text-on-surface flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-error"></span> Algeciras (ESP)</td>
<td class="p-3 text-on-surface-variant">3,100</td>
<td class="p-3 pr-6 text-right text-error font-bold">0.74</td>
</tr>
</tbody>
</table>
</div>
</div>
</div>
</div>
<!-- Bottom padding for scroll -->
<div class="h-8"></div>
</div>
</main>
<!-- BottomNavBar (Mobile Only) -->
<nav class="md:hidden bg-surface-container/40 dark:bg-surface-container/40 backdrop-blur-xl border-t border-white/10 fixed bottom-0 left-0 w-full z-50 flex justify-around items-center h-16 pb-safe">
<a class="flex flex-col items-center justify-center w-full h-full text-on-surface-variant hover:text-primary active:scale-95 transition-all" href="#">
<span class="material-symbols-outlined text-2xl">dashboard</span>
<span class="text-[10px] font-label-md mt-1">Dashboard</span>
</a>
<!-- Active -->
<a class="flex flex-col items-center justify-center w-full h-full text-primary active:scale-95 transition-all relative" href="#">
<div class="absolute -top-3 bg-primary-container text-on-primary-container p-2 rounded-full shadow-lg">
<span class="material-symbols-outlined text-2xl" style="font-variation-settings: 'FILL' 1;">fact_check</span>
</div>
<span class="text-[10px] font-label-md mt-6 font-bold">Audits</span>
</a>
<a class="flex flex-col items-center justify-center w-full h-full text-on-surface-variant hover:text-primary active:scale-95 transition-all" href="#">
<span class="material-symbols-outlined text-2xl">monitoring</span>
<span class="text-[10px] font-label-md mt-1">Telemetry</span>
</a>
</nav>
</body></html>

<!-- User Control & Security Log -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>User Management &amp; Security Logs - Agro-Intelligence Oversight</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Outfit:wght@600;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    colors: {
                        "outline-variant": "#3f4a3f",
                        "surface-container-low": "#171d17",
                        "primary-container": "#3da35d",
                        "surface-container-lowest": "#0a100a",
                        "on-secondary-fixed-variant": "#1e502e",
                        "inverse-on-surface": "#2c322b",
                        "surface-container": "#1b211b",
                        "surface-variant": "#30362f",
                        "surface-container-highest": "#30362f",
                        "inverse-primary": "#006d33",
                        "primary-fixed": "#92f8a9",
                        "on-surface-variant": "#becabc",
                        "tertiary-fixed-dim": "#89ceff",
                        "on-surface": "#dee4da",
                        "surface-tint": "#76db8f",
                        "tertiary-fixed": "#c9e6ff",
                        "on-error-container": "#ffdad6",
                        "on-tertiary-fixed": "#001e2f",
                        "on-background": "#dee4da",
                        "on-tertiary-fixed-variant": "#004c6e",
                        "error-container": "#93000a",
                        "secondary-container": "#205331",
                        "primary-fixed-dim": "#76db8f",
                        "on-secondary-container": "#8fc599",
                        "on-primary-container": "#003114",
                        "tertiary": "#89ceff",
                        "surface-bright": "#343b34",
                        "secondary": "#9dd3a7",
                        "on-primary-fixed": "#00210b",
                        "on-tertiary": "#00344d",
                        "on-primary": "#003918",
                        "secondary-fixed": "#b8f0c2",
                        "background": "#0f150f",
                        "outline": "#889487",
                        "tertiary-container": "#009ada",
                        "primary": "#76db8f",
                        "on-tertiary-container": "#002d43",
                        "surface-container-high": "#252c25",
                        "surface-dim": "#0f150f",
                        "on-error": "#690005",
                        "inverse-surface": "#dee4da",
                        "surface": "#0f150f",
                        "on-secondary-fixed": "#00210c",
                        "on-primary-fixed-variant": "#005225",
                        "on-secondary": "#01391a",
                        "secondary-fixed-dim": "#9dd3a7",
                        "error": "#ffb4ab"
                    },
                    borderRadius: {
                        "DEFAULT": "0.125rem",
                        "lg": "0.25rem",
                        "xl": "0.5rem",
                        "full": "0.75rem"
                    },
                    spacing: {
                        "gutter": "16px",
                        "card-gap": "20px",
                        "container-padding": "24px",
                        "unit": "4px"
                    },
                    fontFamily: {
                        "body-md": ["Inter", "sans-serif"],
                        "headline-sm": ["Outfit", "sans-serif"],
                        "body-sm": ["Inter", "sans-serif"],
                        "headline-md": ["Outfit", "sans-serif"],
                        "display-lg": ["Outfit", "sans-serif"],
                        "headline-lg": ["Outfit", "sans-serif"],
                        "mono-data": ["monospace"],
                        "label-md": ["Inter", "sans-serif"],
                        "body-lg": ["Inter", "sans-serif"]
                    },
                    fontSize: {
                        "body-md": ["16px", { "lineHeight": "24px", "fontWeight": "400" }],
                        "headline-sm": ["20px", { "lineHeight": "28px", "fontWeight": "600" }],
                        "body-sm": ["14px", { "lineHeight": "20px", "fontWeight": "400" }],
                        "headline-md": ["24px", { "lineHeight": "32px", "fontWeight": "600" }],
                        "display-lg": ["48px", { "lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "700" }],
                        "headline-lg": ["32px", { "lineHeight": "40px", "fontWeight": "600" }],
                        "mono-data": ["14px", { "lineHeight": "20px", "fontWeight": "500" }],
                        "label-md": ["12px", { "lineHeight": "16px", "letterSpacing": "0.05em", "fontWeight": "600" }],
                        "body-lg": ["18px", { "lineHeight": "28px", "fontWeight": "400" }]
                    }
                }
            }
        }
    </script>
<style>
        body { background-color: #0c120c; color: #dee4da; }
        .glass-panel {
            background-color: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .glass-panel-active {
            background-color: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(40px);
            border: 1px solid rgba(61, 163, 93, 0.5);
            box-shadow: 0 0 30px rgba(61, 163, 93, 0.15);
        }
        .pulse-critical {
            animation: pulse-border 2s infinite;
        }
        @keyframes pulse-border {
            0% { border-color: rgba(255, 180, 171, 0.5); box-shadow: 0 0 0 0 rgba(255, 180, 171, 0.4); }
            70% { border-color: rgba(255, 180, 171, 1); box-shadow: 0 0 0 6px rgba(255, 180, 171, 0); }
            100% { border-color: rgba(255, 180, 171, 0.5); box-shadow: 0 0 0 0 rgba(255, 180, 171, 0); }
        }
    </style>
</head>
<body class="min-h-screen flex overflow-hidden">
<!-- SideNavBar -->
<nav class="h-screen w-20 hover:w-64 transition-all duration-300 ease-in-out fixed left-0 top-0 z-50 bg-surface-container-lowest border-r border-white/5 shadow-2xl flex flex-col py-6 h-full group overflow-hidden">
<div class="px-6 mb-8 flex items-center space-x-4 flex-shrink-0">
<span class="material-symbols-outlined text-primary-fixed" style="font-variation-settings: 'FILL' 1;">terminal</span>
<div class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">
<h1 class="font-headline-sm text-headline-sm text-primary-fixed">AUDIT_OS_V1</h1>
<p class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Terminal Active</p>
</div>
</div>
<div class="flex-1 space-y-2">
<a class="flex items-center space-x-4 px-6 py-3 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg transition-all duration-300" href="#">
<span class="material-symbols-outlined flex-shrink-0">dashboard</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Dashboard</span>
</a>
<a class="flex items-center space-x-4 px-6 py-3 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg transition-all duration-300" href="#">
<span class="material-symbols-outlined flex-shrink-0">security_update_warning</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Risk Analysis</span>
</a>
<a class="flex items-center space-x-4 px-6 py-3 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg transition-all duration-300" href="#">
<span class="material-symbols-outlined flex-shrink-0">monitoring</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Telemetry</span>
</a>
<a class="flex items-center space-x-4 px-6 py-3 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg transition-all duration-300" href="#">
<span class="material-symbols-outlined flex-shrink-0">fact_check</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Audits</span>
</a>
<a class="flex items-center space-x-4 px-6 py-3 bg-primary-container text-on-primary-container rounded-lg mx-2 transition-all duration-300" href="#">
<span class="material-symbols-outlined flex-shrink-0">settings</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Settings</span>
</a>
</div>
<div class="mt-auto space-y-2">
<button class="w-full flex items-center space-x-4 px-6 py-3 text-primary mx-2 hover:bg-surface-variant/20 rounded-lg transition-all duration-300">
<span class="material-symbols-outlined flex-shrink-0">download</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Export Report</span>
</button>
<div class="border-t border-white/5 my-2 mx-4"></div>
<a class="flex items-center space-x-4 px-6 py-3 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg transition-all duration-300" href="#">
<span class="material-symbols-outlined flex-shrink-0">help</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Support</span>
</a>
<a class="flex items-center space-x-4 px-6 py-3 text-on-surface-variant hover:text-primary mx-2 hover:bg-surface-variant/20 rounded-lg transition-all duration-300" href="#">
<span class="material-symbols-outlined flex-shrink-0">logout</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Logout</span>
</a>
</div>
</nav>
<!-- Main Content Area -->
<main class="ml-20 flex-1 flex flex-col h-screen overflow-hidden transition-all duration-300">
<!-- TopAppBar Placeholder (Using specific styles requested) -->
<header class="bg-surface-container/40 backdrop-blur-xl border-b border-white/10 shadow-sm flex justify-between items-center px-container-padding w-full h-16 flex-shrink-0 z-40">
<div class="flex items-center gap-8">
<div class="font-headline-md text-headline-md font-bold text-primary">Agro-Intelligence Oversight</div>
</div>
<div class="flex items-center gap-4">
<button class="text-on-surface-variant hover:text-primary transition-colors cursor-pointer active:scale-95">
<span class="material-symbols-outlined">notifications</span>
</button>
<button class="text-on-surface-variant hover:text-primary transition-colors cursor-pointer active:scale-95">
<span class="material-symbols-outlined">settings</span>
</button>
<div class="h-8 w-8 rounded-full overflow-hidden border border-white/10">
<img alt="Auditor Profile" class="w-full h-full object-cover" data-alt="A macro shot of a stylized, futuristic profile avatar in a dark tech environment. The avatar features abstract geometric patterns glowing with subtle green telemetry lines against a deep charcoal background. The lighting is clinical and high-contrast, emphasizing precision and security. The overall mood is vigilant and highly advanced, fitting an agro-industrial auditor's digital identity." src="https://lh3.googleusercontent.com/aida-public/AB6AXuDqoe6o6iqxq8mQrdO81XPqEWYx7_uq6edjKbtTx5J9omHdD-7CWX5BchVzS83uHE2z6I6R5ZkWLDdfx9Wi0MsBGJivMjrH_6kPpi3KxqDhQAeB8cqEVNDiTxxsNv32gExK-_QygyVHDPXLPEOWPe9pJfnYPlSjBkt54okbwECfGm5TWMwQ782q32s2wAfcsW46E4L3bQufMRlv99RETLB2rMXis6e8kDTOJ5ErJW4G4LFztDh0HkfmTpYeB1EQeueieBTx2MmOzwU"/>
</div>
</div>
</header>
<!-- Canvas -->
<div class="flex-1 overflow-y-auto p-container-padding @container">
<div class="max-w-7xl mx-auto space-y-card-gap">
<!-- Header -->
<div class="flex justify-between items-end border-b border-white/10 pb-4">
<div>
<h2 class="font-headline-lg text-headline-lg text-on-surface mb-1">User Management</h2>
<p class="font-body-md text-body-md text-on-surface-variant">System access control and telemetry oversight.</p>
</div>
<div class="flex gap-4">
<button class="glass-panel px-4 py-2 rounded-lg font-label-md text-label-md text-on-surface hover:border-primary transition-colors flex items-center gap-2">
<span class="material-symbols-outlined text-[18px]">add</span>
                             NEW OPERATIVE
                         </button>
</div>
</div>
<!-- Main Layout Grid -->
<div class="grid grid-cols-1 @4xl:grid-cols-12 gap-card-gap">
<!-- Left Column: User Table (Spans 8 cols on large screens) -->
<div class="@4xl:col-span-8 space-y-card-gap">
<div class="glass-panel rounded-xl overflow-hidden flex flex-col h-[600px]">
<div class="p-4 border-b border-white/10 bg-surface-container/20 flex justify-between items-center">
<h3 class="font-headline-sm text-headline-sm text-on-surface">Operative Registry</h3>
<div class="relative">
<span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-[18px]">search</span>
<input class="bg-transparent border border-white/10 rounded-lg pl-9 pr-4 py-1.5 font-body-sm text-body-sm text-on-surface focus:border-primary focus:ring-0 focus:outline-none transition-colors w-64 glass-panel" placeholder="Search operatives..." type="text"/>
</div>
</div>
<div class="flex-1 overflow-auto">
<table class="w-full text-left border-collapse">
<thead class="sticky top-0 bg-surface-container-high/80 backdrop-blur-md border-b-2 border-primary z-10">
<tr>
<th class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider py-3 px-4">Operative</th>
<th class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider py-3 px-4">Clearance</th>
<th class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider py-3 px-4">Protocol</th>
<th class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider py-3 px-4">Status</th>
<th class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider py-3 px-4">Actions</th>
</tr>
</thead>
<tbody class="font-mono-data text-mono-data text-on-surface divide-y divide-white/5">
<!-- Row 1 -->
<tr class="hover:bg-white/[0.02] transition-colors group">
<td class="py-3 px-4">
<div class="flex items-center gap-3">
<div class="w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center font-bold text-primary">JD</div>
<div>
<div class="font-body-sm text-body-sm text-on-surface">J. Doe</div>
<div class="text-[10px] text-on-surface-variant opacity-70">T-minus 2m</div>
</div>
</div>
</td>
<td class="py-3 px-4 text-primary">ADMIN</td>
<td class="py-3 px-4">Cond. A</td>
<td class="py-3 px-4">
<span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-sm bg-primary/10 text-primary border border-primary/20 text-[11px]">
<span class="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span> ACTIVE
                                                </span>
</td>
<td class="py-3 px-4">
<div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
<button class="p-1 text-on-surface-variant hover:text-primary transition-colors" title="Change Condition"><span class="material-symbols-outlined text-[18px]">swap_horiz</span></button>
<button class="p-1 text-on-surface-variant hover:text-error transition-colors" title="Reset Token"><span class="material-symbols-outlined text-[18px]">lock_reset</span></button>
</div>
</td>
</tr>
<!-- Row 2 -->
<tr class="hover:bg-white/[0.02] transition-colors group">
<td class="py-3 px-4">
<div class="flex items-center gap-3">
<div class="w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center font-bold text-on-surface-variant">AS</div>
<div>
<div class="font-body-sm text-body-sm text-on-surface">A. Smith</div>
<div class="text-[10px] text-on-surface-variant opacity-70">T-minus 4h</div>
</div>
</div>
</td>
<td class="py-3 px-4 text-on-surface-variant">AUDITOR</td>
<td class="py-3 px-4">Cond. B</td>
<td class="py-3 px-4">
<span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-sm bg-primary/10 text-primary border border-primary/20 text-[11px]">
<span class="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span> ACTIVE
                                                </span>
</td>
<td class="py-3 px-4">
<div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
<button class="p-1 text-on-surface-variant hover:text-primary transition-colors" title="Change Condition"><span class="material-symbols-outlined text-[18px]">swap_horiz</span></button>
<button class="p-1 text-on-surface-variant hover:text-error transition-colors" title="Reset Token"><span class="material-symbols-outlined text-[18px]">lock_reset</span></button>
</div>
</td>
</tr>
<!-- Row 3 -->
<tr class="hover:bg-white/[0.02] transition-colors group opacity-60">
<td class="py-3 px-4">
<div class="flex items-center gap-3">
<div class="w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center font-bold text-on-surface-variant">RK</div>
<div>
<div class="font-body-sm text-body-sm text-on-surface">R. Vance</div>
<div class="text-[10px] text-on-surface-variant opacity-70">T-minus 12d</div>
</div>
</div>
</td>
<td class="py-3 px-4 text-on-surface-variant">AUDITOR</td>
<td class="py-3 px-4">-</td>
<td class="py-3 px-4">
<span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-sm bg-surface-variant text-on-surface-variant border border-white/10 text-[11px]">
<span class="w-1.5 h-1.5 rounded-full bg-on-surface-variant"></span> OFFLINE
                                                </span>
</td>
<td class="py-3 px-4">
<div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
<button class="p-1 text-on-surface-variant hover:text-primary transition-colors" title="Change Condition"><span class="material-symbols-outlined text-[18px]">swap_horiz</span></button>
<button class="p-1 text-on-surface-variant hover:text-error transition-colors" title="Reset Token"><span class="material-symbols-outlined text-[18px]">lock_reset</span></button>
</div>
</td>
</tr>
</tbody>
</table>
</div>
</div>
</div>
<!-- Right Column: Security Logs (Spans 4 cols on large screens) -->
<div class="@4xl:col-span-4 space-y-card-gap">
<div class="glass-panel rounded-xl flex flex-col h-[600px] border-t-2 border-t-error">
<div class="p-4 border-b border-white/10 bg-surface-container/20 flex justify-between items-center">
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-error">gpp_bad</span>
<h3 class="font-headline-sm text-headline-sm text-on-surface">Security Telemetry</h3>
</div>
<button class="text-on-surface-variant hover:text-primary transition-colors"><span class="material-symbols-outlined text-[20px]">filter_list</span></button>
</div>
<div class="p-3 bg-surface-container-high/50 border-b border-white/5 flex gap-2">
<select class="bg-surface-variant border-none rounded text-[11px] text-on-surface py-1 pl-2 pr-6 focus:ring-1 focus:ring-primary h-7">
<option>All Events</option>
<option>Logins</option>
<option>Exports</option>
</select>
<select class="bg-surface-variant border-none rounded text-[11px] text-on-surface py-1 pl-2 pr-6 focus:ring-1 focus:ring-primary h-7">
<option>All Severities</option>
<option>Critical</option>
<option>Warning</option>
</select>
</div>
<div class="flex-1 overflow-auto p-4 space-y-3 font-mono-data text-[12px] leading-tight">
<!-- Log Item: Critical -->
<div class="p-3 rounded border border-error/30 bg-error/5 relative overflow-hidden pulse-critical">
<div class="absolute left-0 top-0 bottom-0 w-1 bg-error"></div>
<div class="flex justify-between items-start mb-1 text-on-surface-variant opacity-70">
<span>[14:23:01 UTC]</span>
<span class="text-error font-bold tracking-wider text-[10px]">CRITICAL</span>
</div>
<div class="text-on-surface">Multiple failed auth attempts detected.</div>
<div class="mt-2 text-on-surface-variant flex items-center gap-1">
<span class="material-symbols-outlined text-[14px]">person</span> Target: ADMIN_JD
                                    </div>
</div>
<!-- Log Item: Warning -->
<div class="p-3 rounded border border-secondary/30 bg-secondary/5 relative overflow-hidden">
<div class="absolute left-0 top-0 bottom-0 w-1 bg-secondary"></div>
<div class="flex justify-between items-start mb-1 text-on-surface-variant opacity-70">
<span>[12:05:44 UTC]</span>
<span class="text-secondary font-bold tracking-wider text-[10px]">WARN</span>
</div>
<div class="text-on-surface">Unusual volume data export initiated.</div>
<div class="mt-2 text-on-surface-variant flex items-center gap-1">
<span class="material-symbols-outlined text-[14px]">download</span> Init: AUDITOR_AS
                                    </div>
</div>
<!-- Log Item: Info -->
<div class="p-3 rounded border border-white/10 bg-white/5 relative overflow-hidden">
<div class="absolute left-0 top-0 bottom-0 w-1 bg-outline-variant"></div>
<div class="flex justify-between items-start mb-1 text-on-surface-variant opacity-70">
<span>[11:30:00 UTC]</span>
<span class="text-outline-variant font-bold tracking-wider text-[10px]">INFO</span>
</div>
<div class="text-on-surface">Protocol condition shifted: A -&gt; B.</div>
<div class="mt-2 text-on-surface-variant flex items-center gap-1">
<span class="material-symbols-outlined text-[14px]">settings_backup_restore</span> Exec: SYSTEM
                                    </div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</main>
</body></html>

<!-- Experimental Telemetry Console -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Experimental Telemetry Dashboard (Admin)</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Outfit:wght@400;600;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    "colors": {
                            "outline-variant": "#3f4a3f",
                            "surface-container-low": "#171d17",
                            "primary-container": "#3da35d",
                            "surface-container-lowest": "#0a100a",
                            "on-secondary-fixed-variant": "#1e502e",
                            "inverse-on-surface": "#2c322b",
                            "surface-container": "#1b211b",
                            "surface-variant": "#30362f",
                            "surface-container-highest": "#30362f",
                            "inverse-primary": "#006d33",
                            "primary-fixed": "#92f8a9",
                            "on-surface-variant": "#becabc",
                            "tertiary-fixed-dim": "#89ceff",
                            "on-surface": "#dee4da",
                            "surface-tint": "#76db8f",
                            "tertiary-fixed": "#c9e6ff",
                            "on-error-container": "#ffdad6",
                            "on-tertiary-fixed": "#001e2f",
                            "on-background": "#dee4da",
                            "on-tertiary-fixed-variant": "#004c6e",
                            "error-container": "#93000a",
                            "secondary-container": "#205331",
                            "primary-fixed-dim": "#76db8f",
                            "on-secondary-container": "#8fc599",
                            "on-primary-container": "#003114",
                            "tertiary": "#89ceff",
                            "surface-bright": "#343b34",
                            "secondary": "#9dd3a7",
                            "on-primary-fixed": "#00210b",
                            "on-tertiary": "#00344d",
                            "on-primary": "#003918",
                            "secondary-fixed": "#b8f0c2",
                            "background": "#0f150f",
                            "outline": "#889487",
                            "tertiary-container": "#009ada",
                            "primary": "#76db8f",
                            "on-tertiary-container": "#002d43",
                            "surface-container-high": "#252c25",
                            "surface-dim": "#0f150f",
                            "on-error": "#690005",
                            "inverse-surface": "#dee4da",
                            "surface": "#0f150f",
                            "on-secondary-fixed": "#00210c",
                            "on-primary-fixed-variant": "#005225",
                            "on-secondary": "#01391a",
                            "secondary-fixed-dim": "#9dd3a7",
                            "error": "#ffb4ab"
                    },
                    "borderRadius": {
                            "DEFAULT": "0.125rem",
                            "lg": "0.25rem",
                            "xl": "0.5rem",
                            "full": "0.75rem"
                    },
                    "spacing": {
                            "gutter": "16px",
                            "card-gap": "20px",
                            "container-padding": "24px",
                            "unit": "4px"
                    },
                    "fontFamily": {
                            "body-md": [
                                    "Inter"
                            ],
                            "headline-sm": [
                                    "Outfit"
                            ],
                            "body-sm": [
                                    "Inter"
                            ],
                            "headline-md": [
                                    "Outfit"
                            ],
                            "display-lg": [
                                    "Outfit"
                            ],
                            "headline-lg": [
                                    "Outfit"
                            ],
                            "mono-data": [
                                    "monospace"
                            ],
                            "label-md": [
                                    "Inter"
                            ],
                            "body-lg": [
                                    "Inter"
                            ]
                    },
                    "fontSize": {
                            "body-md": [
                                    "16px",
                                    {
                                            "lineHeight": "24px",
                                            "fontWeight": "400"
                                    }
                            ],
                            "headline-sm": [
                                    "20px",
                                    {
                                            "lineHeight": "28px",
                                            "fontWeight": "600"
                                    }
                            ],
                            "body-sm": [
                                    "14px",
                                    {
                                            "lineHeight": "20px",
                                            "fontWeight": "400"
                                    }
                            ],
                            "headline-md": [
                                    "24px",
                                    {
                                            "lineHeight": "32px",
                                            "fontWeight": "600"
                                    }
                            ],
                            "display-lg": [
                                    "48px",
                                    {
                                            "lineHeight": "56px",
                                            "letterSpacing": "-0.02em",
                                            "fontWeight": "700"
                                    }
                            ],
                            "headline-lg": [
                                    "32px",
                                    {
                                            "lineHeight": "40px",
                                            "fontWeight": "600"
                                    }
                            ],
                            "mono-data": [
                                    "14px",
                                    {
                                            "lineHeight": "20px",
                                            "fontWeight": "500"
                                    }
                            ],
                            "label-md": [
                                    "12px",
                                    {
                                            "lineHeight": "16px",
                                            "letterSpacing": "0.05em",
                                            "fontWeight": "600"
                                    }
                            ],
                            "body-lg": [
                                    "18px",
                                    {
                                            "lineHeight": "28px",
                                            "fontWeight": "400"
                                    }
                            ]
                    }
            },
                },
        }
    </script>
<style>
        body {
            background-color: #0c120c;
        }
        .glass-panel {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .glass-panel-active {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(40px);
            -webkit-backdrop-filter: blur(40px);
            border: 1px solid rgba(61, 163, 93, 0.5);
            box-shadow: 0 0 30px rgba(61, 163, 93, 0.15);
        }
        .table-row-hover:hover {
            background: rgba(255, 255, 255, 0.08);
        }
        .pulse-border {
            animation: pulse-border 2s infinite;
        }
        @keyframes pulse-border {
            0% { border-color: rgba(61, 163, 93, 0.5); box-shadow: 0 0 0 0 rgba(61, 163, 93, 0.4); }
            70% { border-color: rgba(61, 163, 93, 0); box-shadow: 0 0 0 10px rgba(61, 163, 93, 0); }
            100% { border-color: rgba(61, 163, 93, 0); box-shadow: 0 0 0 0 rgba(61, 163, 93, 0); }
        }
    </style>
</head>
<body class="text-on-surface font-body-md min-h-screen flex flex-col md:flex-row overflow-x-hidden">
<!-- Mobile TopNavBar (visible only on md:hidden) -->
<nav class="md:hidden bg-surface-container/40 dark:bg-surface-container/40 backdrop-blur-xl docked full-width top-0 border-b border-white/10 shadow-sm flex justify-between items-center px-container-padding w-full h-16 z-50">
<div class="font-headline-md text-headline-md font-bold text-primary">Agro-Intelligence Oversight</div>
<div class="flex items-center gap-4">
<span class="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors cursor-pointer active:scale-95" data-icon="notifications">notifications</span>
<span class="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors cursor-pointer active:scale-95" data-icon="settings">settings</span>
</div>
</nav>
<!-- SideNavBar (visible on md:flex) -->
<nav class="hidden md:flex flex-col py-6 h-full bg-surface-container-lowest dark:bg-surface-container-lowest h-screen w-20 hover:w-64 transition-all duration-300 ease-in-out fixed left-0 top-0 z-50 border-r border-white/5 shadow-2xl group">
<div class="px-4 mb-8 flex items-center gap-4 overflow-hidden whitespace-nowrap">
<img alt="System Logo" class="w-10 h-10 rounded-full object-cover border border-white/10 shrink-0" data-alt="A highly detailed, ultra-minimalist vector logo of a geometric shield or abstract data core, utilizing a clinical palette of deep charcoal green and vibrant primary emerald accents. The design should convey a sense of absolute security, technological vigilance, and precision auditing. It must be isolated on a pure black background." src="https://lh3.googleusercontent.com/aida-public/AB6AXuDktUrwRrFeIEd9bh3Gt5iV3camJXenQnWsA-ry5ApLp6T1RxrANx_1WcgQ8cmdI1M51-LYvz8R-J6RJc-97Jh1QTTKZfysv6sABavWE2to6qnnzynOlbcPqYob7pSPjyG6DgNbLmf2YsEFk7Dge6kyhHF34zomLrjSzHAHlds3AmTBpY-hIHYbIA1VPF3R_2NgArXXQ4vMjsJBSwyhMOuy0Oh7mex4PlZrg-Tee3jeXPY6_Hxbh4F73YpS_F3mo5w19RBZWKVkvxw"/>
<div class="flex flex-col opacity-0 group-hover:opacity-100 transition-opacity duration-300">
<span class="font-headline-sm text-headline-sm text-primary-fixed">AUDIT_OS_V1</span>
<span class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">Terminal Active</span>
</div>
</div>
<div class="flex-1 flex flex-col gap-2 overflow-hidden">
<a class="flex items-center gap-4 py-3 px-4 mx-2 text-on-surface-variant hover:text-primary hover:bg-surface-variant/20 transition-all duration-300 rounded-lg group/item" href="#">
<span class="material-symbols-outlined shrink-0" data-icon="dashboard">dashboard</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Dashboard</span>
</a>
<a class="flex items-center gap-4 py-3 px-4 mx-2 text-on-surface-variant hover:text-primary hover:bg-surface-variant/20 transition-all duration-300 rounded-lg group/item" href="#">
<span class="material-symbols-outlined shrink-0" data-icon="security_update_warning">security_update_warning</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Risk Analysis</span>
</a>
<a class="flex items-center gap-4 py-3 px-4 mx-2 bg-primary-container text-on-primary-container rounded-lg transition-all duration-300 group/item" href="#">
<span class="material-symbols-outlined shrink-0" data-icon="monitoring">monitoring</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Telemetry</span>
</a>
<a class="flex items-center gap-4 py-3 px-4 mx-2 text-on-surface-variant hover:text-primary hover:bg-surface-variant/20 transition-all duration-300 rounded-lg group/item" href="#">
<span class="material-symbols-outlined shrink-0" data-icon="fact_check">fact_check</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Audits</span>
</a>
<a class="flex items-center gap-4 py-3 px-4 mx-2 text-on-surface-variant hover:text-primary hover:bg-surface-variant/20 transition-all duration-300 rounded-lg group/item" href="#">
<span class="material-symbols-outlined shrink-0" data-icon="settings">settings</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Settings</span>
</a>
</div>
<div class="px-4 mt-auto mb-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 overflow-hidden whitespace-nowrap">
<button class="w-full bg-primary/20 hover:bg-primary/30 text-primary border border-primary/50 font-label-md text-label-md uppercase tracking-wider py-2 rounded-lg transition-colors flex items-center justify-center gap-2">
<span class="material-symbols-outlined" data-icon="download">download</span> Export Report
            </button>
</div>
<div class="flex flex-col gap-2 border-t border-white/5 pt-4 overflow-hidden">
<a class="flex items-center gap-4 py-2 px-4 mx-2 text-on-surface-variant hover:text-primary hover:bg-surface-variant/20 transition-all duration-300 rounded-lg group/item" href="#">
<span class="material-symbols-outlined shrink-0" data-icon="help">help</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Support</span>
</a>
<a class="flex items-center gap-4 py-2 px-4 mx-2 text-on-surface-variant hover:text-error hover:bg-error/10 transition-all duration-300 rounded-lg group/item" href="#">
<span class="material-symbols-outlined shrink-0" data-icon="logout">logout</span>
<span class="font-label-md text-label-md uppercase tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">Logout</span>
</a>
</div>
</nav>
<!-- Main Content Canvas -->
<main class="flex-1 md:ml-20 p-container-padding max-w-[1600px] mx-auto w-full transition-all duration-300 relative z-10">
<!-- Header Section -->
<header class="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
<div>
<h1 class="font-display-lg text-display-lg text-on-surface">Experimental Telemetry</h1>
<p class="font-body-lg text-body-lg text-on-surface-variant mt-2 max-w-2xl">Real-time analysis of decision matrices and comprehension vectors across active A/B testing protocols.</p>
</div>
<div class="flex gap-4">
<button class="glass-panel px-6 py-3 rounded-lg flex items-center gap-2 text-primary hover:bg-primary/10 transition-colors border-primary/30">
<span class="material-symbols-outlined" data-icon="file_download">file_download</span>
<span class="font-label-md text-label-md uppercase tracking-wider">Export JSON</span>
</button>
<button class="bg-primary text-on-primary px-6 py-3 rounded-lg flex items-center gap-2 hover:bg-primary-fixed transition-colors font-label-md text-label-md uppercase tracking-wider shadow-[0_0_15px_rgba(118,219,143,0.3)] hover:shadow-[0_0_25px_rgba(118,219,143,0.5)]">
<span class="material-symbols-outlined" data-icon="table_view">table_view</span>
                    Export CSV
                </button>
</div>
</header>
<!-- Bento Grid Layout -->
<div class="grid grid-cols-1 md:grid-cols-12 gap-card-gap">
<!-- KPI: Avg Decision Time -->
<div class="glass-panel rounded-xl p-6 md:col-span-6 lg:col-span-3 flex flex-col relative overflow-hidden">
<div class="absolute inset-0 opacity-20 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-primary-container via-transparent to-transparent pointer-events-none"></div>
<div class="flex justify-between items-start mb-4">
<h3 class="font-label-md text-label-md uppercase tracking-wider text-on-surface-variant">Avg. Decision Time</h3>
<span class="material-symbols-outlined text-primary" data-icon="timer">timer</span>
</div>
<div class="flex items-end gap-4 mt-auto">
<div>
<div class="font-label-md text-label-md text-on-surface-variant mb-1">Condition A</div>
<div class="font-display-lg text-display-lg text-error">65<span class="font-headline-sm text-headline-sm text-on-surface-variant ml-1">s</span></div>
</div>
<div class="h-12 w-[1px] bg-white/10 mb-2"></div>
<div>
<div class="font-label-md text-label-md text-on-surface-variant mb-1">Condition B</div>
<div class="font-display-lg text-display-lg text-primary">42<span class="font-headline-sm text-headline-sm text-on-surface-variant ml-1">s</span></div>
</div>
</div>
<div class="mt-4 h-1 w-full bg-white/5 rounded-full overflow-hidden flex">
<div class="bg-error h-full" style="width: 60%"></div>
<div class="bg-primary h-full" style="width: 40%"></div>
</div>
</div>
<!-- KPI: Avg Comprehension -->
<div class="glass-panel rounded-xl p-6 md:col-span-6 lg:col-span-3 flex flex-col relative overflow-hidden">
<div class="absolute inset-0 opacity-20 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-tertiary-container via-transparent to-transparent pointer-events-none"></div>
<div class="flex justify-between items-start mb-4">
<h3 class="font-label-md text-label-md uppercase tracking-wider text-on-surface-variant">Avg. Comprehension</h3>
<span class="material-symbols-outlined text-tertiary" data-icon="psychology">psychology</span>
</div>
<div class="flex items-end gap-4 mt-auto">
<div>
<div class="font-label-md text-label-md text-on-surface-variant mb-1">Condition A</div>
<div class="font-display-lg text-display-lg text-tertiary">4.8<span class="font-headline-sm text-headline-sm text-on-surface-variant ml-1">/5</span></div>
</div>
<div class="h-12 w-[1px] bg-white/10 mb-2"></div>
<div>
<div class="font-label-md text-label-md text-on-surface-variant mb-1">Condition B</div>
<div class="font-display-lg text-display-lg text-error">2.1<span class="font-headline-sm text-headline-sm text-on-surface-variant ml-1">/5</span></div>
</div>
</div>
<div class="mt-4 flex gap-1">
<div class="h-1 flex-1 bg-tertiary rounded-full"></div>
<div class="h-1 flex-1 bg-tertiary rounded-full"></div>
<div class="h-1 flex-1 bg-tertiary rounded-full"></div>
<div class="h-1 flex-1 bg-tertiary rounded-full"></div>
<div class="h-1 flex-1 bg-white/10 rounded-full"></div>
</div>
</div>
<!-- Boxplot Visualization -->
<div class="glass-panel rounded-xl p-6 md:col-span-12 lg:col-span-6 flex flex-col">
<div class="flex justify-between items-center mb-6">
<h3 class="font-headline-sm text-headline-sm text-on-surface">Decision Times by Condition</h3>
<span class="material-symbols-outlined text-on-surface-variant" data-icon="candlestick_chart">candlestick_chart</span>
</div>
<div class="flex-1 relative min-h-[200px] flex items-center justify-center">
<!-- Abstract representation of a boxplot using styled divs -->
<div class="w-full h-full flex flex-col justify-between py-4 relative">
<!-- Y-axis labels -->
<div class="absolute left-0 top-0 bottom-0 flex flex-col justify-between font-mono-data text-mono-data text-on-surface-variant text-xs">
<span>80s</span>
<span>60s</span>
<span>40s</span>
<span>20s</span>
<span>0s</span>
</div>
<!-- Grid lines -->
<div class="absolute left-8 right-0 top-0 border-t border-white/5 h-1/4"></div>
<div class="absolute left-8 right-0 top-1/4 border-t border-white/5 h-1/4"></div>
<div class="absolute left-8 right-0 top-2/4 border-t border-white/5 h-1/4"></div>
<div class="absolute left-8 right-0 top-3/4 border-t border-white/5 h-1/4"></div>
<div class="absolute left-8 right-0 bottom-0 border-t border-white/20"></div>
<!-- Boxplots container -->
<div class="absolute left-8 right-0 top-0 bottom-0 flex justify-around items-end pb-8">
<!-- Boxplot A -->
<div class="relative w-16 h-full flex flex-col justify-end items-center group">
<div class="absolute bottom-[20%] h-[60%] w-[1px] bg-error/50"></div> <!-- Whisker -->
<div class="absolute bottom-[20%] w-4 h-[1px] bg-error/50"></div> <!-- Bottom Cap -->
<div class="absolute bottom-[80%] w-4 h-[1px] bg-error/50"></div> <!-- Top Cap -->
<div class="absolute bottom-[40%] w-full h-[30%] bg-error/20 border border-error/50 rounded-sm backdrop-blur-sm transition-all group-hover:bg-error/30">
<div class="absolute top-[40%] w-full h-[2px] bg-error shadow-[0_0_5px_rgba(255,180,171,0.8)]"></div> <!-- Median -->
</div>
<span class="absolute -bottom-6 font-label-md text-label-md text-on-surface-variant">Cond. A</span>
</div>
<!-- Boxplot B -->
<div class="relative w-16 h-full flex flex-col justify-end items-center group">
<div class="absolute bottom-[10%] h-[50%] w-[1px] bg-primary/50"></div> <!-- Whisker -->
<div class="absolute bottom-[10%] w-4 h-[1px] bg-primary/50"></div> <!-- Bottom Cap -->
<div class="absolute bottom-[60%] w-4 h-[1px] bg-primary/50"></div> <!-- Top Cap -->
<div class="absolute bottom-[25%] w-full h-[25%] bg-primary/20 border border-primary/50 rounded-sm backdrop-blur-sm transition-all group-hover:bg-primary/30">
<div class="absolute top-[60%] w-full h-[2px] bg-primary shadow-[0_0_5px_rgba(118,219,143,0.8)]"></div> <!-- Median -->
</div>
<span class="absolute -bottom-6 font-label-md text-label-md text-on-surface-variant">Cond. B</span>
</div>
</div>
</div>
</div>
</div>
<!-- Scatter Plot Visualization -->
<div class="glass-panel rounded-xl p-6 md:col-span-12 lg:col-span-4 flex flex-col">
<div class="flex justify-between items-center mb-6">
<h3 class="font-headline-sm text-headline-sm text-on-surface">Comprehension vs Time</h3>
<span class="material-symbols-outlined text-on-surface-variant" data-icon="scatter_plot">scatter_plot</span>
</div>
<div class="flex-1 relative min-h-[250px] bg-surface-container-low/50 rounded-lg border border-white/5 p-4 overflow-hidden">
<!-- Abstract Scatter Plot -->
<div class="absolute bottom-4 left-4 right-4 h-[1px] bg-white/20"></div> <!-- X axis -->
<div class="absolute bottom-4 left-4 top-4 w-[1px] bg-white/20"></div> <!-- Y axis -->
<span class="absolute bottom-0 right-4 font-mono-data text-[10px] text-on-surface-variant">Time (s)</span>
<span class="absolute top-4 left-0 -rotate-90 font-mono-data text-[10px] text-on-surface-variant origin-left">Comp.</span>
<!-- Data Points (Condition A - Red) -->
<div class="absolute top-[20%] left-[60%] w-2 h-2 rounded-full bg-error shadow-[0_0_5px_rgba(255,180,171,0.8)] animate-pulse" style="animation-delay: 0.1s"></div>
<div class="absolute top-[15%] left-[70%] w-2 h-2 rounded-full bg-error shadow-[0_0_5px_rgba(255,180,171,0.8)] animate-pulse" style="animation-delay: 0.3s"></div>
<div class="absolute top-[25%] left-[65%] w-2 h-2 rounded-full bg-error shadow-[0_0_5px_rgba(255,180,171,0.8)] animate-pulse" style="animation-delay: 0.5s"></div>
<div class="absolute top-[10%] left-[80%] w-2 h-2 rounded-full bg-error shadow-[0_0_5px_rgba(255,180,171,0.8)] animate-pulse" style="animation-delay: 0.2s"></div>
<!-- Data Points (Condition B - Green) -->
<div class="absolute top-[60%] left-[30%] w-2 h-2 rounded-full bg-primary shadow-[0_0_5px_rgba(118,219,143,0.8)] animate-pulse" style="animation-delay: 0.4s"></div>
<div class="absolute top-[75%] left-[20%] w-2 h-2 rounded-full bg-primary shadow-[0_0_5px_rgba(118,219,143,0.8)] animate-pulse" style="animation-delay: 0.6s"></div>
<div class="absolute top-[50%] left-[40%] w-2 h-2 rounded-full bg-primary shadow-[0_0_5px_rgba(118,219,143,0.8)] animate-pulse" style="animation-delay: 0.1s"></div>
<div class="absolute top-[80%] left-[15%] w-2 h-2 rounded-full bg-primary shadow-[0_0_5px_rgba(118,219,143,0.8)] animate-pulse" style="animation-delay: 0.7s"></div>
<!-- Trend Lines -->
<svg class="absolute inset-0 w-full h-full pointer-events-none" style="z-index: -1;">
<line stroke="rgba(118,219,143,0.2)" stroke-dasharray="4" stroke-width="2" x1="10%" x2="45%" y1="90%" y2="40%"></line>
<line stroke="rgba(255,180,171,0.2)" stroke-dasharray="4" stroke-width="2" x1="50%" x2="90%" y1="30%" y2="10%"></line>
</svg>
</div>
</div>
<!-- Participant Progress Table -->
<div class="glass-panel rounded-xl p-0 md:col-span-12 lg:col-span-8 flex flex-col overflow-hidden">
<div class="p-6 border-b border-white/5 flex justify-between items-center bg-surface-container-low/30">
<div>
<h3 class="font-headline-sm text-headline-sm text-on-surface">Real-time Participant Progress</h3>
<p class="font-body-sm text-body-sm text-on-surface-variant mt-1">Live telemetry stream from active testing nodes.</p>
</div>
<div class="flex items-center gap-2">
<span class="relative flex h-3 w-3">
<span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
<span class="relative inline-flex rounded-full h-3 w-3 bg-primary"></span>
</span>
<span class="font-mono-data text-mono-data text-primary">LIVE</span>
</div>
</div>
<div class="overflow-x-auto">
<table class="w-full text-left border-collapse">
<thead>
<tr class="bg-white/[0.02] border-b border-primary/30">
<th class="py-3 px-6 font-label-md text-label-md uppercase tracking-wider text-on-surface-variant">Subject ID</th>
<th class="py-3 px-6 font-label-md text-label-md uppercase tracking-wider text-on-surface-variant">Active Condition</th>
<th class="py-3 px-6 font-label-md text-label-md uppercase tracking-wider text-on-surface-variant">Sessions</th>
<th class="py-3 px-6 font-label-md text-label-md uppercase tracking-wider text-on-surface-variant">Success Rate</th>
<th class="py-3 px-6 font-label-md text-label-md uppercase tracking-wider text-on-surface-variant text-right">Status</th>
</tr>
</thead>
<tbody class="font-mono-data text-mono-data divide-y divide-white/5">
<tr class="table-row-hover transition-colors">
<td class="py-4 px-6 text-on-surface">USR-8492-X</td>
<td class="py-4 px-6"><span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-error/10 text-error border border-error/20">Condition A</span></td>
<td class="py-4 px-6 text-on-surface-variant">12 / 15</td>
<td class="py-4 px-6">
<div class="flex items-center gap-2">
<div class="w-16 bg-white/10 rounded-full h-1.5">
<div class="bg-error h-1.5 rounded-full" style="width: 45%"></div>
</div>
<span class="text-error">45%</span>
</div>
</td>
<td class="py-4 px-6 text-right"><span class="material-symbols-outlined text-on-surface-variant text-sm animate-spin" data-icon="sync">sync</span></td>
</tr>
<tr class="table-row-hover transition-colors glass-panel-active rounded-lg m-1 relative z-10">
<td class="py-4 px-6 text-primary font-bold">USR-7731-Y</td>
<td class="py-4 px-6"><span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary/10 text-primary border border-primary/20 pulse-border">Condition B</span></td>
<td class="py-4 px-6 text-on-surface">14 / 15</td>
<td class="py-4 px-6">
<div class="flex items-center gap-2">
<div class="w-16 bg-white/10 rounded-full h-1.5">
<div class="bg-primary h-1.5 rounded-full" style="width: 92%"></div>
</div>
<span class="text-primary">92%</span>
</div>
</td>
<td class="py-4 px-6 text-right"><span class="material-symbols-outlined text-primary text-sm" data-icon="warning">warning</span></td>
</tr>
<tr class="table-row-hover transition-colors">
<td class="py-4 px-6 text-on-surface">USR-9011-Z</td>
<td class="py-4 px-6"><span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-error/10 text-error border border-error/20">Condition A</span></td>
<td class="py-4 px-6 text-on-surface-variant">15 / 15</td>
<td class="py-4 px-6">
<div class="flex items-center gap-2">
<div class="w-16 bg-white/10 rounded-full h-1.5">
<div class="bg-on-surface-variant h-1.5 rounded-full" style="width: 55%"></div>
</div>
<span class="text-on-surface-variant">55%</span>
</div>
</td>
<td class="py-4 px-6 text-right"><span class="material-symbols-outlined text-tertiary text-sm" data-icon="check_circle">check_circle</span></td>
</tr>
<tr class="table-row-hover transition-colors">
<td class="py-4 px-6 text-on-surface">USR-4420-W</td>
<td class="py-4 px-6"><span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary/10 text-primary border border-primary/20">Condition B</span></td>
<td class="py-4 px-6 text-on-surface-variant">03 / 15</td>
<td class="py-4 px-6">
<div class="flex items-center gap-2">
<div class="w-16 bg-white/10 rounded-full h-1.5">
<div class="bg-primary h-1.5 rounded-full" style="width: 88%"></div>
</div>
<span class="text-primary">88%</span>
</div>
</td>
<td class="py-4 px-6 text-right"><span class="material-symbols-outlined text-on-surface-variant text-sm animate-spin" data-icon="sync">sync</span></td>
</tr>
</tbody>
</table>
</div>
</div>
</div>
</main>
</body></html>