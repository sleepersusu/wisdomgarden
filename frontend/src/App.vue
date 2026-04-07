<template>
  <div id="app-root">
    <nav class="navbar">
      <RouterLink to="/" class="brand">WisdomGarden Cart</RouterLink>
      <div class="nav-links">
        <RouterLink to="/" class="nav-link">
          <ShoppingCart :size="18" />
          Cart
        </RouterLink>
        <RouterLink to="/orders" class="nav-link">
          <ClipboardList :size="18" />
          Orders
        </RouterLink>
      </div>
    </nav>
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { ShoppingCart, ClipboardList } from 'lucide-vue-next'
</script>

<style scoped>
#app-root { min-height: 100vh; display: flex; flex-direction: column; }

.navbar {
  background: var(--color-surface);
  border-bottom: 1.5px solid var(--color-border);
  padding: 0 2rem;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 10;
}

.brand {
  font-family: 'Rubik', sans-serif;
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--color-primary);
  text-decoration: none;
}

.nav-links { display: flex; gap: 0.5rem; }

.nav-link {
  display: flex; align-items: center; gap: 0.4rem;
  padding: 0.4rem 0.9rem; border-radius: 0.5rem;
  color: var(--color-muted); text-decoration: none;
  font-weight: 600; font-size: 0.9rem;
  transition: background-color var(--transition), color var(--transition);
}

.nav-link:hover, .nav-link.router-link-active {
  background-color: #cffafe;
  color: var(--color-primary);
}

.main-content { flex: 1; padding: 2rem; max-width: 1100px; width: 100%; margin: 0 auto; }
</style>
