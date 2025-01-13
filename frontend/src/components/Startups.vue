<script setup>
import {onMounted, reactive, useTemplateRef} from "vue";
import {getData, user, startups} from "@/shared/modules.js"

const confirmation_block = useTemplateRef('confirmation_block')
const main = useTemplateRef('main')
const option = reactive({
  "input":"",
  'block_btn': false
})

onMounted(() => {
  document.title = 'Стартапы';
});
</script>
<template>
  <div class="confirmation_block fixed" ref="confirmation_block">
    <h3>Напишите почему вы откликнулись</h3>
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
              main.style.filter = "blur(0px)";'>Отмена</button>
      <button class="send-btn mini-btn" @click="
        option.block_btn = true;
      " ref="">Отправить</button>
    </div>
  </div>

  <div ref="main">
    <h1 class="title">Каталог стартапов</h1>

    <div class="center-block-auth anime-opacity-smooth" v-for="startup in startups">
      <img class="text-auth img-startup" :src="startup.picture" alt="Картинка отсутствует">
      <h2>Название: {{ startup.name }}</h2>
      <p class="text-auth">{{ startup.description }}</p>
      <button class="send-btn" @click="main.style.filter = 'blur(5px)';
        option.block_btn = true;
        confirmation_block.style.display = 'flex'"
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