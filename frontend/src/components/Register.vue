<script setup>
import { onMounted, reactive, useTemplateRef } from 'vue';

const btn = useTemplateRef('btn')

const form = reactive({
  username: "",
  email: "",
  password: "",
  description: "",
})

function OnClick() {
  btn.value.classList.add('btn-loading', 'loading')
  btn.value.innerHTML = "Загрузка"
}

onMounted(() => {
  document.title = 'Регистация';
});
</script>

<template>
    <div class="center-block-auth anime-opacity-smooth">
      <h2 class="text-hello">Добро пожаловать!</h2>
      <p class="text-auth">Регистрация</p>
      <section>
        <div class="section-input form__group field">
          <input class="form__field" type="text" id="username" placeholder="Name" :value="form.username"
            @input="event => form.username = event.target.value"/>
          <label class="between-block form__label" for="username">Ваше имя:</label>
        </div>

        <div class="section-input form__group field">
          <input class="form__field" type="text" id="email" placeholder="Email" :value="form.email"
            @input="event => form.email = event.target.value"/>
          <label class="between-block form__label" for="email">Ваша почта:</label>
        </div>

        <div class="section-input form__group field">
          <input class="form__field" type="password" id="password" placeholder="Password" :value="form.password"
            @input="event => form.password = event.target.value"/>
          <label class="between-block form__label" for="password">Придумайте пароль:</label>
        </div>

        <div class="section-input form__group field">
          <textarea class="form__field description-edit" type="text" id="description" placeholder="Description" :value="form.description"
            @input="event => form.description = event.target.value"/>
          <label class="between-block form__label" for="description">Немного о себе:</label>
        </div>

        <div class="section-btn">
          <button class="send-btn" @click="OnClick()" ref="btn"
            :disabled="form.password.length === 0
            || form.email.length === 0
            || form.description.length === 0
            || form.username.length === 0">
            Зарегистрироваться</button>
        </div>
      </section>
    </div>
</template>


<style scoped>

</style>