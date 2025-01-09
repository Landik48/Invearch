<script setup>

</script>

<template>
  <nav>
    <RouterLink to="/" class="router-text">Главная</RouterLink>
    <RouterLink to="/startups" class="router-text">Стартапы</RouterLink>
    <RouterLink to="/profile" class="router-text">Профиль</RouterLink>
    <RouterLink to="/auth" class="router-text">Авторизация</RouterLink>
  </nav>
  <main>
    <RouterView />
  </main>
</template>

<style scoped>
  nav {
    width: 100%;
    height: 50px;
    text-decoration: none;
    display: flex;
    justify-content: space-around;
    align-items: center;
    background-color: rgb(173, 173, 173);
    border-radius: 15px;
  }
</style>