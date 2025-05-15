<script setup>
import { Form, Field } from "vee-validate";
import { ref } from "vue";
import * as Yup from "yup";
import axios from "axios";
import ImageHolder from "../assets/image3.jpg";
import css from "../assets/base.css";
const showText = ref(true);

async function onSubmit(values) {
  if (values.document) {
    console.log(">>>>>>>>>>>> " + values.document);
    const params = new URLSearchParams();
    params.append("query", values.document);
    axios
      .post("http://localhost:8000/searchimage/" + params.toString())
      .then((res) => {
        if (res.status === false) {
          // Handle the error here...
          console.log(">>>>>>>>>>>> success");
        } else {
          // Handle the user data here...
          console.log(">>>>>>>> " + res.data.URL);
          //document.getElementById("answer").innerHTML = res.data.URL;
          //imgvar = res.data.URL;

          const imgElement = document.getElementById('imageSearchResult');
          imgElement.src = res.data.URL;
          
          showText.value = true;
        }
      });
  }
}
</script>

<template>
  <div class="d-flex align-items-center justify-content-center w-100">
    <div class="card w-50 h-40">
      <h4 class="card-header">Image Search</h4>
      <div class="card-body">
        <Form
          @submit="onSubmit"
          :validation-schema="schema"
          v-slot="{ isSubmitting }"
        >
          <div class="form-group">
            <label>Query</label>
            <Field name="document" type="text" class="form-control" />
          </div>
          <div class="form-group">
            <button
              @click="changeValue"
              class="btn btn-primary"
              :disabled="isSubmitting"
            >
              <span
                v-show="isSubmitting"
                class="spinner-border spinner-border-sm mr-1"
              ></span
              >Search
            </button>
            <br />
            <label class="mt-4">Search Result</label>
            <div
              id="answer"
              style="
                border: 1px solid #ddd;
                cborder-radius: 5px;
                padding: 20px 5px;
                background: black;
                color: #fff;
                font-size: 13px;
              "
            >
            <div style="position: relative">
              <img id="imageSearchResult" :src="ImageHolder" class="h-50 w-50"/>
            </div>
          </div>
          </div>
          <div class="form-group"></div>
        </Form>
      </div>
    </div>
  </div>
</template>
<style>
/* Styling for the "Open Popup" button */
.open-popup-button {
  padding: 10px 10px;
  font-size: 16px;
  background-color: #2f30316a;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.open-popup-button:hover {
  background-color: #0056b3;
}

.open-popup-button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.3);
}
</style>
