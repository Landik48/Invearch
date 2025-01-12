<script setup>
import {getUser, user} from "@/shared/modules.js"
import {ref, useTemplateRef} from "vue";
import { useRouter } from 'vue-router';

const btn = useTemplateRef('btn')
const confirmation_block = useTemplateRef('confirmation')
const router = useRouter();
const confirmation = ref("")
const main = useTemplateRef('main')

async function OnClick(option) {
  btn.value.classList.add('loading')
  btn.value.innerHTML = "Загрузка"
  const response = await fetch(`http://localhost/api/users/user/`, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    body: JSON.stringify({"option": option}),
    }
  });
  if (response.status === 200) {
    btn.value.style.backgroundColor = "#38ef7d"
    btn.value.innerHTML = "Успешно!"
    btn.value.classList.remove('loading')
    setTimeout(() => {
      router.push('/auth')
    }, 1000)
    await getUser()
  } else {
    alert("Неуспешная операция, попробуйте позже")
  }
}
</script>

<template>
  <div class="confirmation_block" ref='confirmation'>
    <h3>Напишите ваше имя для подтверждения</h3>
    <div class="section-input form__group field">
      <input class="form__field" type="text" id="confirmation" placeholder="Confirmation"
             :value="confirmation.value"
             @input="event => confirmation.value = event.target.value"/>
      <label class="between-block form__label" for="confirmation">{{ user.username }}</label>
      <button class="send-btn mini-btn"
              @click='
              confirmation.value = " ";
              confirmation_block.style.display = "none";
              main.style.filter = "blur(0px)";'
              ref="btn">Отмена</button>
      <button class="exit-btn mini-btn" @click="OnClick('delete')" ref="btn"
      :disabled="confirmation.value != user.username">Удалить аккаунт</button>
    </div>
  </div>
  <div class="main" ref="main">
    <div class="block-user">
      <h3>Имя: {{ user.username }}</h3>
      <h3>Актуальная почта: {{ user.email }} </h3>
      <p><h3>Обо мне:</h3> {{ user.description }}</p>
      <div class="group_btns">
        <button class="exit-btn" @click="OnClick('exit')">Выход</button>
        <button class="exit-btn"
          @click="main.style.filter = 'blur(5px)'; confirmation_block.style.display = 'flex'">Удалить аккаунт</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.main {
  width: 100%;
  display: flex;
  justify-content: center;
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
</style>