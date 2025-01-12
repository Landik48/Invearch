<script setup>
import {getCookie, getUser, user} from "@/shared/modules.js"
import {computed, reactive, ref, useTemplateRef} from "vue";
import { useRouter } from 'vue-router';

const btn_del = useTemplateRef('btn_del')
const btn_exit = useTemplateRef('btn_exit')
const btn_edit = useTemplateRef('btn_edit')
const confirmation_block = useTemplateRef('confirmation_block')
const router = useRouter();
const main = useTemplateRef('main')
const csrfToken = getCookie('csrftoken')

const option = reactive({
  "option": "",
  "input":""
})

const isButtonDisabled = computed(() => {
  return option.input !== user.value.username;
});

const form = reactive({
  username: "",
  email: "",
  description: "",
  password: ""
})

async function OnClick(option_el, btn) {
  btn.classList.add('loading');
  btn.innerHTML = "Загрузка";
  let response = null
  if (option_el !== "edit") {
    option.option = option_el
    response = await fetch(`http://localhost/api/users/user/`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken || '',
      },
      body: JSON.stringify(option),
    });

    if (response.status !== 200) {
      alert("Неуспешная операция, попробуйте позже")
    }
  } else {
    response = await fetch(`http://localhost/api/users/user/`, {
      method: 'PUT',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken || '',
      },
      body: JSON.stringify(form),})

    const data = await response.json()
    if (response.status !== 200) {
      btn.classList.remove('loading');
      btn.style.background = "red"
      btn.innerHTML = data
      setTimeout(() => {
        btn.style.background = "#9b9b9b"
        btn.innerHTML = "Изменить"
      }, 2000)
    }
  }
  if (response.status === 200) {
    btn.style.backgroundColor = "#38ef7d"
    btn.innerHTML = "Успешно!"
    btn.classList.remove('loading')
    setTimeout(() => {
      router.push('/auth')
    }, 1000)
    await getUser()
  }
}
</script>

<template>
  <div class="confirmation_block" ref="confirmation_block">
    <h3>Напишите ваше имя для подтверждения</h3>
    <div class="section-input form__group field">
      <input class="form__field" type="text" id="confirmation" placeholder="Confirmation"
             v-model="option.input"
             @input="event => option.input = event.target.value"/>
      <label class="between-block form__label" for="confirmation">{{ user.username }}</label>
      <button class="send-btn mini-btn cancel-btn"
              @click='
              option.input = "";
              confirmation_block.style.display = "none";
              main.style.filter = "blur(0px)";'
              >Отмена</button>
      <button class="exit-btn mini-btn" @click="OnClick('delete', btn_del)" ref="btn_del"
      :disabled="isButtonDisabled">Удалить аккаунт</button>
    </div>
  </div>
  <div class="main" ref="main">
    <div class="block-user">
      <h2 class="title">Пользователь</h2>
      <h3>Имя: {{ user.username }}</h3>
      <h3>Актуальная почта: {{ user.email }} </h3>
      <p><h3>Обо мне:</h3> {{ user.description }}</p><br>
      <h3>Мои стартапы:</h3>
      <p class="line-startups" v-for="startup in user.startups"> - {{ startup }}</p>
      <div class="group_btns">
        <button class="exit-btn" @click="OnClick('exit', btn_exit)" ref="btn_exit">Выход</button>
        <button class="exit-btn"
          @click="main.style.filter = 'blur(5px)'; confirmation_block.style.display = 'flex'">Удалить аккаунт</button>
      </div>
    </div>

    <div class="block-user">
      <h2 class="title">Изменение данных</h2>
      <h4 class="title">
        <span style="color: red">Важно!</span>
        на редактирование данных отправляются данные всех форм
      </h4>
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
        <label class="between-block form__label" for="password">Изменяемый пароль:</label>
      </div>

      <div class="section-input form__group field">
          <textarea class="form__field description-edit" type="text" id="description" placeholder="Description" :value="form.description"
                    @input="event => form.description = event.target.value"/>
        <label class="between-block form__label" for="description">Немного о себе:</label>
      </div>

      <div class="section-btn">
        <button class="send-btn edit-btn" @click="OnClick('edit', btn_edit)" ref="btn_edit"
                :disabled="form.password.length === 0
            || form.email.length === 0
            || form.description.length === 0
            || form.username.length === 0">
          Изменить</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.main {
  width: 100%;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.block-user {
  margin-top: 40px;
  border-radius: 10px;
  padding: 20px;
  width: 90%;
  display: flex;
  background-color: rgba(0,43,54,1);
  flex-wrap: wrap;
  max-width: 800px;
}

h3 {
  width: 100%;
}
p {
  margin: 0;
}

.exit-btn {
  font-size: 16px;
  background-color: red;
  border: none;
  border-radius: 5px;
  width: 200px;
  height: 50px;
  margin: 10px;
  transition: .3s;
  transform: scale(1);
  filter: grayscale(30%);
}

.exit-btn:hover {
  filter: grayscale(0%);
  transition: .3s;
  transform: scale(0.95);
}

.group_btns {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  width: 100%;
}

.send-btn {
  width: 200px;
}

.confirmation_block {
  width: 70%;
  max-width: 800px;
  background-color: rgba(0,43,54,1);
  border-radius: 10px;
  padding: 10px;
  display: none;
  justify-content: center;
  flex-wrap: wrap;
  text-align: center;
  position: absolute;
  z-index: 100;
  margin: auto;
  height: fit-content;
  top: 0; left: 0; bottom: 0; right: 0;
}

h3 {
  margin-bottom: 0;
}

.exit-btn:disabled {
  background-color: #9b9b9b;
}

.cancel-btn {
  background-color: #0eb855;
}

.title {
  text-align: center;
  width: 100%;
}

p {
  width: 100%;
}

.line-startups {
  margin-left: 20px;
  margin-top: 10px;
}

.section-btn {
  width: 100%;
  display: flex;
  justify-content: center;
}
</style>