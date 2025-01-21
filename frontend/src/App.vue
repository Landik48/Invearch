<script setup>
import { onMounted, ref, useTemplateRef, onBeforeUnmount } from 'vue';
import {user, getData, startups} from '@/shared/modules.js'
import Adaptive_links from "@/components/modules/adaptive_links.vue";
import adaptive_links from "@/components/modules/adaptive_links.vue";

const loading = ref(false)
const load_el = useTemplateRef('loading')
const scroll_flag = ref(null)
const containerRef = ref(null);
const up_block = useTemplateRef('up-block')
const nav_view = ref(false)
let isMobile = ref(window.matchMedia("(max-width:500px)").matches);
const nav_block = useTemplateRef('nav_block')

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

function BorderEdit(el) {
  if (nav_view.value) {
    el.style.borderRadius = '15px 15px 0 0'
  } else {
    el.style.borderRadius = '15px'
  }
}

onMounted(() => {
  updateUser();

  window.addEventListener('resize', () => {
    isMobile.value = window.matchMedia("(max-width:500px)").matches;
  });

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

  <nav class="anime-opacity-smooth nav-adaptive" ref="scroll_flag">
    <img @click="nav_view = !nav_view;BorderEdit($event.target.parentElement)"
         class="svg-up burger margin" src="../src/components/icons/burger.svg" alt="">
    <Adaptive_links :user="user" :loading="loading" v-if="!isMobile"></Adaptive_links>
  </nav>
  <Adaptive_links :user="user" :loading="loading" v-if="isMobile && nav_view" ref="nav_block"></Adaptive_links>

  <div class="up-block anime-to_up" ref="up-block">
    <img class="svg-up" src="../src/components/icons/to_up.svg" alt="" @click="scrollToTop" />
  </div>

  <main>
    <RouterView />
  </main>
</template>

<style scoped>
  nav {
    margin: 0 auto;
    width: 90%;
    height: 50px;
    text-decoration: none;
    display: flex;
    align-items: center;
    justify-content: space-around;
    background-color: var(--header);
    border-radius: 15px;
    max-width: 1200px;
  }

  .burger {
    display: none;
    width: 40px;
    height: 40px;
  }

  @media (max-width: 500px) {
    .margin {
      margin: 0px 20px 0px 20px;
    }

    .nav-adaptive {
      justify-content: space-between;
    }

    .burger {
      display: block;
    }

    .adaptive-links {
      width: 90%;
      margin: 0 auto;
      background-color: var(--header);
      border-radius: 0 0 15px 15px;
      flex-wrap: wrap;
      padding: 10px;
      box-sizing: border-box;
    }

    .adaptive-links > * {
      margin-right: 5px;
      margin-left: 5px;
    }
  }

</style>