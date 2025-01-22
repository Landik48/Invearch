<script setup>
import {getData, sendData, startups, user} from "@/shared/modules.js"
import {computed, onMounted, reactive, ref, useTemplateRef} from "vue";
import { useRouter } from 'vue-router';

const btn_del = useTemplateRef('btn_del')
const btn_exit = useTemplateRef('btn_exit')
const btn_edit = useTemplateRef('btn_edit')
const btn_create = useTemplateRef('btn_create')
const confirmation_block = useTemplateRef('confirmation_block')
const router = useRouter();
const main = useTemplateRef('main')
const activeIndex = ref(false)

const option = reactive({
  "option": "",
  "input":""
})

const isButtonDisabled = computed(() => {
  return option.input !== user.value.username;
});

const form_user = reactive({
  username: user.value.username,
  email: user.value.email,
  social_networks: user.value.social_networks,
  description: user.value.description,
  password: ""
})

const form_startup = reactive({
  name: "",
  description: "",
  picture: ""
})

function error(btn, data, textbtn){
    btn.classList.remove('loading');
    btn.style.background = "red"
    btn.innerHTML = data
    setTimeout(() => {
      btn.style.background = "#9b9b9b"
      btn.innerHTML = textbtn
    }, 2000)
}

async function OnClick(option_el, btn, form) {
  btn.classList.add('loading');
  btn.innerHTML = "Загрузка";
  let response = null;

  if (option_el === 'create') {
    response = await sendData(`http://localhost/api/startups/`, form)
    const data = response.data
    if (response.status !== 201){
      error(btn, data, "Создать")
    }

  } else if (option_el === 'delete_startup') {
    const form_delete = {}
    response = await sendData(`http://localhost/api/startups/startup/${form}/`, form_delete, 'DELETE')
    await getData(startups, 'startups')
    if (response.status !== 200) {
      alert("Неуспешная операция, попробуйте позже")
    }
  } else if (option_el !== "edit") {
    option.option = option_el
    response = await sendData(`http://localhost/api/users/user/`, option)
    if (response.status !== 200) {
      alert("Неуспешная операция, попробуйте позже")
    }
  } else {
    response = await sendData(`http://localhost/api/users/user/`, form, 'PUT')
    const data = response.data
    error(btn, data, "Изменить")
  }

  if (response.status === 200 || response.status === 201) {
    btn.style.backgroundColor = "#38ef7d"
    btn.innerHTML = "Успешно!"
    btn.classList.remove('loading')

    if (option_el === 'create') {
      setTimeout(() => {
        btn.style.background = "#9b9b9b"
        btn.innerHTML = "Создать"
        form_startup.picture = ''
        form_startup.description = ''
        form_startup.name = ''
      }, 2000)
      await getData(startups, 'startups')
    } else if (option_el !== 'delete_startup') {
      setTimeout(() => {
        router.push('/auth')
      }, 1000)
    }

    await getData(user, 'user')
  }
}

const toggleBlock = (index) => {
  activeIndex.value = activeIndex.value === index ? null : index;
};

onMounted(() => {
  document.title = 'Профиль';
});
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
      <button class="exit-btn mini-btn" @click="OnClick('delete', btn_del, form_user)" ref="btn_del"
      :disabled="isButtonDisabled">Удалить аккаунт</button>
    </div>
  </div>
  <div class="main" ref="main">
    <div class="block-user anime-opacity-smooth">
      <h2 class="title">Пользователь</h2>
      <h3>Имя: {{ user.username }}</h3>
      <h3>Актуальная почта: {{ user.email }} </h3>
      <p><h3>Мои контакты:</h3> {{ user.social_networks }}</p><br>
      <p><h3>Обо мне:</h3> {{ user.description }}</p><br>
      <h3>Мои стартапы:</h3>
      <p>(нажмите, чтобы увидеть отклики)</p>
      <ul class="user-ul" v-if="Boolean(user.my_startups[0])">
        <p class="line-startups block-description" style="text-align: left"
           v-for="(startup, index) in user.my_startups">
          <li>
            <p @click="toggleBlock(index)">
              <i>{{ startup[1] }}</i>
            </p>
            <div class="interesed-block" v-if="activeIndex === index">
              <p class="margin" v-if="Boolean(startup[2][0])">Отклики:</p>
              <p v-if="!Boolean(startup[2][0])"><i>Нет откликов</i></p>
              <ol v-if="Boolean(startup[2][0])">
                <li class="margin" v-for="user_startup in startup[2]">
                  {{user_startup.username}}
                  <p class="margin"><i>О пользователе</i>: {{user_startup.description}}</p>
                  <p class="margin"><i>Соцсети:</i> {{user_startup.social_networks}}</p>
                  <p class="margin"><i>Сообщение:</i> {{user_startup.message}}</p>
                </li>
              </ol>
              <button class="exit-btn mini-btn"
                      @click="OnClick('delete_startup', $event.target, startup[0])"
                      ref="btn-delete-startup">Удалить стартап</button>
            </div>
          </li>
        </p>
      </ul>
      <p class="margin" v-if="!Boolean(user.my_startups[0])"><i>- Данные отсутствуют</i></p>
      <h3>Мои отклики:</h3>
      <ul v-if="Boolean(user.my_parties[0])">
        <li v-for="startup in user.my_parties">
          <p class="line-startups block-description" style="text-align: left">{{ startup[1] }}</p>
        </li>
      </ul>
      <p class="margin" v-if="!Boolean(user.my_parties[0])"><i>- Данные отсутствуют</i></p>
      <div class="group_btns">
        <button class="exit-btn" @click="OnClick('exit', btn_exit, form_user)" ref="btn_exit">Выход</button>
        <button class="exit-btn"
          @click="main.style.filter = 'blur(5px)'; confirmation_block.style.display = 'flex'">Удалить аккаунт</button>
      </div>
    </div>

    <div class="block-user anime-opacity-smooth">
      <h2 class="title">Создание стартапа</h2>
      <div class="section-input form__group field">
        <input class="form__field" type="text" id="name" placeholder="Name" :value="form_startup.name"
               @input="event => form_startup.name = event.target.value"/>
        <label class="between-block form__label" for="name">Название</label>
      </div>

      <div class="section-input form__group field">
          <textarea class="form__field description-edit" type="text" id="description_startup" placeholder="Description" :value="form_startup.description"
                    @input="event => form_startup.description = event.target.value"/>
        <label class="between-block form__label" for="description_startup">Описание стартапа</label>
      </div>

      <div class="section-input form__group field">
        <input class="form__field" type="text" id="link" placeholder="Link" :value="form_startup.picture"
               @input="event => form_startup.picture = event.target.value"/>
        <label class="between-block form__label" for="link">Ссылка на картинку</label>
      </div>

      <div class="section-btn">
        <button class="send-btn edit-btn"
                @click="OnClick('create', btn_create, form_startup)" ref="btn_create"
                :disabled="form_startup.picture.length === 0
            || form_startup.description.length === 0
            || form_startup.name.length === 0">
          Создать</button>
      </div>
    </div>

    <div class="block-user anime-opacity-smooth">
      <h2 class="title">Изменение данных</h2>
      <h4 class="title">
        <span style="color: red">Важно!</span>
        На редактирование данных отправляются данные всех форм
      </h4>
      <div class="section-input form__group field">
        <input class="form__field" type="text" id="username" placeholder="Name" :value="form_user.username"
               @input="event => form_user.username = event.target.value"/>
        <label class="between-block form__label" for="username">Ваше имя</label>
      </div>

      <div class="section-input form__group field">
        <input class="form__field" type="text" id="email" placeholder="Email" :value="form_user.email"
               @input="event => form_user.email = event.target.value"/>
        <label class="between-block form__label" for="email">Ваша почта</label>
      </div>

      <div class="section-input form__group field">
        <input class="form__field" type="password" id="password" placeholder="Password" :value="form_user.password"
               @input="event => form_user.password = event.target.value"/>
        <label class="between-block form__label" for="password">Изменяемый пароль</label>
      </div>

      <div class="section-input form__group field">
        <input class="form__field" type="text" id="contacts" placeholder="Contacts" :value="form_user.social_networks"
               @input="event => form_user.social_networks = event.target.value"/>
        <label class="between-block form__label" for="contacts">Ваши соцсети</label>
      </div>

      <div class="section-input form__group field">
          <textarea class="form__field description-edit" type="text" id="description" placeholder="Description" :value="form_user.description"
                    @input="event => form_user.description = event.target.value"/>
        <label class="between-block form__label" for="description">Немного о себе</label>
      </div>

      <div class="section-btn">
        <button class="send-btn edit-btn" @click="OnClick('edit', btn_edit, form_user)" ref="btn_edit"
                :disabled="form_user.password.length === 0
            || form_user.email.length === 0
            || form_user.description.length === 0
            || form_user.username.length === 0">
          Изменить</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.main {
  max-width: 1200px;
  margin: 20px auto;
  width: 90%;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.block-user {
  max-width: 1200px;
  border-radius: 20px;
  padding: 20px;
  box-sizing: border-box;
  margin: 20px 0;
  width: 100%;
  display: flex;
  box-shadow: 0px 0px 20px rgba(128, 128, 128, 0.2);
  flex-wrap: wrap;
}

h3 {
  width: 100%;
}
p {
  margin: 0;
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

h3 {
  margin-bottom: 0;
}

.exit-btn:disabled {
  background-color: #9b9b9b;
}

.cancel-btn {
  background-color: #0eb855;
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

.margin {
  margin-top: 5px;
}

.user-ul {
  margin-top: 0;
  padding: 15px;
}

@media (max-width: 500px) {
  .user-ul {
    padding: 5px;
  }
  .line-startups {
    margin-left: 10px;
    margin-top: 5px;
  }
}
</style>