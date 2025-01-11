<script setup>
import { onMounted, ref, useTemplateRef } from 'vue';

const user = ref(null);
const loading = ref(false)
const load_el = useTemplateRef('loading')

const getUser = async () => {
  loading.value = true

  try {
    const response = await fetch(`http://localhost/api/users/user/`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
    });
    if (response.status === 403) {
      user.value = null
    } else if (!response.ok) {
      alert("Ошибка на стороне сервера, повторите попытку позже")
      throw new Error('Network response was not ok');
    } else {
      user.value = await response.json();
    }
  } catch {
    alert("Ошибка на стороне сервера, повторите попытку позже")
  }

  let opacity = 1;
  const interval = setInterval(() => {
    opacity -= 0.1;
    if (opacity <= 0) {
        clearInterval(interval);
        loading.value = false
    }
    load_el.value.style.opacity = opacity;
  }, 50);
}

onMounted(() => {
  getUser(); 
});
</script>


<template>
  <head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap" rel="stylesheet">
  </head>
  <nav class="anime-opacity-smooth">
    <RouterLink to="/" class="router-text">Главная</RouterLink>
    <RouterLink to="/startups" class="router-text">Стартапы</RouterLink>
    <RouterLink to="/profile" class="router-text smooth-appearance" v-if="user != null && !loading">Профиль</RouterLink>
    <RouterLink to="/auth" class="router-text smooth-appearance" v-if="user == null && !loading">Авторизация</RouterLink>
    <div class="loading router-text" v-if="loading" ref="loading">Соединение</div>
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
    background-color: rgba(0,43,54,1);
    border-radius: 15px;
  }
</style>