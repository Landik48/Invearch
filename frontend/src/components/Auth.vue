<script setup>
import { onMounted, reactive, useTemplateRef, ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import {user, getData, sendData} from '@/shared/modules.js'

const btn = useTemplateRef('btn')
const data = ref(null)
const router = useRouter()

const form = reactive({
  email: "",
  password: "",
})

async function OnClick() {
  btn.value.classList.add('btn-loading', 'loading')
  btn.value.innerHTML = "Загрузка"
  const response = await sendData(`http://localhost/api/users/auth/`, form)
  data.value = response.data
  if (response.status === 200) {
    btn.value.style.backgroundColor = "#38ef7d"
    setTimeout(() => {
      router.push('/')

    }, 1000)
    await getData(user, 'user')
  } else {
    btn.value.style.backgroundColor = "red"
    setTimeout(() => {
      btn.value.style.backgroundColor = "#9b9b9b"
      btn.value.innerHTML = "Войти"
      form.password = ""
    }, 2000)
  }
  btn.value.classList.remove('btn-loading', 'loading')
  btn.value.innerHTML = data.value
}

onMounted(() => {
  document.title = 'Авторизация';
});
</script>

<template>
    <div class="center-block-auth anime-opacity-smooth">
      <h2 class="text-hello">Добро пожаловать!</h2>
      <p class="text-auth">Авторизация</p>
      <section>
        <div class="section-input form__group field">
          <input class="form__field" type="text" id="email" placeholder="Email" :value="form.email"
                 @input="event => form.email = event.target.value"/>
          <label class="between-block form__label" for="email">Ваша почта</label>
        </div>

        <div class="section-input form__group field">
          <input class="form__field" type="password" id="password" placeholder="Password" :value="form.password"
                 @input="event => form.password = event.target.value"/>
          <label class="between-block form__label" for="password">Ваш пароль</label>
        </div>

        <p><i>Нет аккаунта?
          <RouterLink to="/register" class="register-in-auth">Зарегистрироваться</RouterLink></i>
        </p>

        <div class="section-btn">
          <button class="send-btn" @click="OnClick()" ref="btn"
              :disabled="form.password.length === 0 || form.email.length === 0">Войти</button>
        </div>
      </section>
    </div>
</template>