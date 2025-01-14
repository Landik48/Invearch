<script setup>
import { onMounted, ref, useTemplateRef, onBeforeUnmount } from 'vue';
import {user, getData, startups} from '@/shared/modules.js'

const loading = ref(false)
const load_el = useTemplateRef('loading')
const scroll_flag = ref(null)
const containerRef = ref(null);
const up_block = useTemplateRef('up-block')

const handleIntersection = (entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) {
      up_block.value.classList.remove('anime-to_down')
      up_block.value.style.display = 'block';
    } else {
      up_block.value.classList.add('anime-to_down')
      setTimeout(() => {
        up_block.value.style.display = 'none';
      }, 500)

    }
  });
};

const updateUser = async () => {
  loading.value = true
  await getData(user, 'user')
  await getData(startups, 'startups')
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

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
};

onMounted(() => {
  updateUser();

  const observer = new IntersectionObserver(handleIntersection, {
    root: containerRef.value,
    threshold: 0.1,
  });

  if (scroll_flag.value) {
    observer.observe(scroll_flag.value);
  }

  onBeforeUnmount(() => {
    if (scroll_flag.value) {
      observer.unobserve(scroll_flag.value);
    }
  });
});
</script>


<template>
  <head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap" rel="stylesheet">
  </head>
  <nav class="anime-opacity-smooth" ref="scroll_flag">
    <RouterLink to="/" class="router-text">Главная</RouterLink>
    <RouterLink to="/startups" class="router-text">Стартапы</RouterLink>
    <RouterLink to="/profile" class="router-text smooth-appearance" v-if="user != null && !loading">Профиль</RouterLink>
    <RouterLink to="/auth" class="router-text smooth-appearance" v-if="user == null && !loading">Авторизация</RouterLink>
    <div class="loading router-text" v-if="loading" ref="loading">Соединение</div>
  </nav>

  <div class="up-block anime-to_up" ref="up-block">
    <img class="svg-up" src="../src/components/icons/to_up.svg" alt="" @click="scrollToTop" />
  </div>

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
    max-width: 840px;
    margin: 0 auto;
  }
</style>