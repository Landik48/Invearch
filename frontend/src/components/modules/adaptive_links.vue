<script>
export default {
  props: {
    user: {
      type: Object,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<template>
  <div class="adaptive-links anime-from-up">
    <RouterLink to="/" class="router-text smooth-appearance">Главная</RouterLink>
    <RouterLink to="/startups" class="router-text color-blue smooth-appearance">Стартапы</RouterLink>
    <RouterLink to="/profile" class="router-text smooth-appearance" v-if="user != null && !loading">Профиль</RouterLink>
    <RouterLink to="/auth" class="router-text smooth-appearance" v-if="user == null && !loading">Авторизация</RouterLink>
    <div class="loading router-text margin smooth-appearance" v-if="loading" ref="loading">Соединение</div>
  </div>
</template>