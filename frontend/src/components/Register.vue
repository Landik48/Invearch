<script setup>
import {onMounted, reactive, ref, useTemplateRef} from 'vue';
import {getCookie, getData, user} from "@/shared/modules.js";
import { useRouter } from 'vue-router';

const btn = useTemplateRef('btn')
const data = ref(null)
const router = useRouter()
const csrfToken = getCookie('csrftoken')

const form = reactive({
  username: "",
  email: "",
  password: "",
  description: "",
})

async function OnClick() {
  btn.value.classList.add('btn-loading', 'loading')
  btn.value.innerHTML = "Загрузка"
  const response = await fetch(`http://localhost/api/users/register/`, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken || '',
    },
    body: JSON.stringify(form),
  });

  data.value = await response.json()
  if (response.status === 200) {
    btn.value.style.backgroundColor = "#38ef7d"
    setTimeout(() => {
      router.push('/auth')

    }, 1000)
    await getData(user, 'user')
  } else {
    btn.value.style.background = "red"
    setTimeout(() => {
      btn.value.style.background = "#9b9b9b"
      btn.value.innerHTML = "Войти"
    }, 2000)
  }
  btn.value.classList.remove('btn-loading', 'loading')
  btn.value.innerHTML = data.value
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