<script setup>
import { onMounted, ref, useTemplateRef } from 'vue';

const user = ref(null);
const loading = ref(false)
const load_el = useTemplateRef('loading')

const getUser = async () => {
  loading.value = true
  try {
    const response = await fetch('http://127.0.0.1:8000/api/users/user');
    // неисправность с получением запрета на доступ к пользователю(не авторизован)
    if (response.ok) {
      const fetchedUser = await response.json();
      user.value = fetchedUser;
      console.log(user.value); 
    } else if (response.status == 301) {

    }
  } catch {
    alert("Ошибка на стороне сервера, попробуйте позже")
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
  document.title = 'Главная';
  getUser(); 
});
</script>


<template>
  <nav>
    <RouterLink to="/" class="router-text">Главная</RouterLink>
    <RouterLink to="/startups" class="router-text">Стартапы</RouterLink>
    <RouterLink to="/profile" class="router-text smooth-appearance" v-if="user != null && !loading">Профиль</RouterLink>
    <RouterLink to="/auth" class="router-text smooth-appearance" v-if="user == null && !loading">Авторизация</RouterLink>
    <div class="loading router-text" v-if="loading" ref="loading">Проверка профиля...</div>
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