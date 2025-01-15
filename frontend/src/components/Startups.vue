<script setup>
import {onMounted, reactive, useTemplateRef} from "vue";
import {getData, user, startups, sendData} from "@/shared/modules.js"
import {useRouter} from "vue-router";

const confirmation_block = useTemplateRef('confirmation_block')
const main = useTemplateRef('main')
const btn_send = useTemplateRef('btn_send')
const router = useRouter();
const option = reactive({
  "input":"",
  'block_btn': false,
  'startupid': ''
})
const form = reactive({
  message: "",
  userid: "",
})

async function onClick() {
  form.message = option.input
  form.userid = user.value.userid
  const response = await sendData(`http://localhost/api/startups/startup/${option.startupid}/`, form)
  const data = response.data

  if (response.status === 200) {
    btn_send.value.style.backgroundColor = "#38ef7d"
    setTimeout(() => {
      router.push('/profile')
    }, 1000)
    await getData(user, 'user')
  } else {
    btn_send.value.style.background = "red"
    setTimeout(() => {
      btn_send.value.style.background = "#9b9b9b"
      btn_send.value.innerHTML = "Отправить"
      confirmation_block.value.style.display = "none"
      main.value.style.filter = "blur(0px)"
      option.block_btn = false;
      option.input = ""
      option.startupid = ""
    }, 2000)
  }
  option.startupid = '';
  btn_send.value.classList.remove('btn-loading', 'loading')
  btn_send.value.innerHTML = data
}


onMounted(() => {
  document.title = 'Стартапы';
});
</script>
<template>
  <div class="confirmation_block fixed" ref="confirmation_block">
    <h3 style="width: 100%">Почему вы откликнулись?</h3>
    <p><i>Минимум 50 символов</i></p>
    <div class="section-input form__group field">
      <input class="form__field" type="text" id="confirmation" placeholder="Confirmation"
             v-model="option.input"
             @input="event => option.input = event.target.value"/>
      <label class="between-block form__label" for="confirmation">Ваше сообщение</label>
      <button class="exit-btn mini-btn"
              @click='
              option.block_btn = false;
              option.input = "";
              confirmation_block.style.display = "none";
              option.startupid = "";
              main.style.filter = "blur(0px)";'>Отмена</button>
      <button class="send-btn mini-btn"
        :disabled="option.input.length <= 50"
        @click="option.block_btn = true;
        onClick()" ref="btn_send">Отправить</button>
    </div>
  </div>

  <div ref="main">
    <h1 class="title">Каталог стартапов</h1>

    <div class="center-block-auth anime-opacity-smooth" v-for="startup in startups">
      <img class="text-auth img-startup" :src="startup.picture" alt="Картинка отсутствует">
      <h2 class="title">Название: {{ startup.name }}</h2>
      <p class="block-description">{{ startup.description }}</p>
      <button class="send-btn" @click="main.style.filter = 'blur(5px)';
        option.block_btn = true;
        confirmation_block.style.display = 'flex'
        option.startupid = startup.startupid;"
              :disabled="option.block_btn"
              ref="btn">Мне интересно!</button>
    </div>
  </div>
</template>

<style scoped>
.send-btn {
  width: 200px;
}

.img-startup {
  margin-top: 10px;
  width: 200px;
  height: 112px;
  border-radius: 10px;
}

.fixed {
  position: fixed;
}
</style>