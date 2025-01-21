<script setup>
import {onMounted} from "vue";

onMounted(() => {
  document.title = 'Главная';
})
</script>

<template>

  <div id='main'>
    <section class="section" id='hello-page'>
      <div class="hello-page__text" data-aos="zoom-in-right">
        <h1 class="hello-page__text_title title">Startlup</h1>
        <p class="hello-page__text_description description">Loer fjhsj daufg adpfavd fhpvahfvb dhpbaf dfb apdifba dpifads fpiasdbf apdadsfadsfhodvafvda asdg asd fass
          Loer fjhsj daufg adpfavd fhpvahfvb dhpbaf dfb apdifba dpifads fpiasdbf apdadsfadsfhodvafvda</p>
      </div>
      <img class="hello-page__img" src="../shared/imgs/startap.jpg" data-aos="zoom-in-left">
    </section>

    <section class="section" id='description-page'>
      <h1 class="title description-page__title text-center" data-aos="zoom-in-down">Наши преимущества</h1>
      <div class="description-page__list">
        <div class="description-page__list__item" data-aos="fade-up">
          <h3 class="description-page__list_el"><span class="num">1</span>
            <span class="text-list"> Простота и удобство использования</span></h3>
        </div>
        <div class="description-page__list__item" data-aos="fade-up">
          <h3 class="description-page__list_el"><span class="num">2</span>
            <span class="text-list"> Одни из немногочисленных на рынке</span></h3>
        </div>
        <div class="description-page__list__item" data-aos="fade-up">
          <h3 class="description-page__list_el"><span class="num">3</span>
            <span class="text-list"> Публиковать и откликаться может каждый</span></h3>
        </div>
        <div class="description-page__list__item" data-aos="fade-up">
          <h3 class="description-page__list_el"><span class="num">4</span>
            <span class="text-list"> Поиск без посредников</span></h3>
        </div>
      </div>
    </section>

    <section class="section">
      <h1 class="title loading" data-aos="zoom-in">Но это далеко не всё</h1>
      <h3 class="block-description" data-aos="zoom-in-up">Проект активно развивается и планируется расширение</h3>
      <h3 class="block-description contrast" style="margin-bottom: 40px" data-aos="zoom-in-up">В будущем вас ждёт</h3>
      <div class="description-page__list">
        <div class="description-page__list__item" data-aos="zoom-in-up">
          <h3 class="description-page__list_el"><span class="num">1</span>
            <span class="text-list"> Чат с поддержкой внутри платформы</span></h3>
        </div>
        <div class="description-page__list__item" data-aos="zoom-in-up">
          <h3 class="description-page__list_el"><span class="num">2</span>
            <span class="text-list"> Аватарки у пользователей</span></h3>
        </div>
        <div class="description-page__list__item" data-aos="zoom-in-up">
          <h3 class="description-page__list_el"><span class="num">3</span>
            <span class="text-list"> Рейтинг стартапов и пользователей</span></h3>
        </div>
        <div class="description-page__list__item" data-aos="zoom-in-up">
          <h3 class="description-page__list_el"><span class="num">4</span>
            <span class="text-list"> Фильтрация контента</span></h3>
        </div>
        <div class="description-page__list__item" data-aos="zoom-in-up">
          <h3 class="description-page__list_el"><span class="num">5</span>
            <span class="text-list"> Удобный поиск</span></h3>
        </div>
        <div class="description-page__list__item" data-aos="zoom-in-up">
          <h3 class="description-page__list_el"><span class="num">6</span>
            <span class="text-list"> Оптимизация платформы</span></h3>
        </div>
      </div>
      <h3 class="block-description" style="margin-top: 80px" data-aos="zoom-out-up">Регистрируйтесь прямо
        <RouterLink to="/register"><span class="contrast">сейчас!</span></RouterLink></h3>
    </section>
  </div>
  <hr>
  <footer>
    <h3 class="title-footer"><i>The project was made by Landik</i></h3>
    <h3>2025</h3>
  </footer>
</template>

<style scoped>
@import "../assets/css_modules/main_page.css";
</style>