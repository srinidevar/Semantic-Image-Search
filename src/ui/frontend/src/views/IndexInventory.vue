<script setup>
import { Form, Field } from "vee-validate";
import * as Yup from "yup";
import axios from "axios";

function sendFileAsFormData(file) {
  console.log(">>>>>>>>>>>>> 1");
  // Create a new FormData object
  var formData = new FormData();

  // Read the file content using FileReader
  var reader = new FileReader();
  reader.onload = function (event) {
    var fileContent = event.target.result;
  console.log(">>>>>>>>>>>>> 2");

    // Append the file and file content to the FormData object
    formData.append("file", file);
    formData.append("fileContent", fileContent);

    // Create the Fetch API request
    var request = new Request("http://localhost:8000/indeximage", {
      method: "POST",
      body: formData,
      mode: "no-cors",
    });

    // Send the request
    fetch(request)
      .then(function (response) {
        // Handle the response
        if (response.ok) {
          console.log("File uploaded successfully.");
          // Do something with the successful response
        }
      })
      .catch(function (error) {
        console.error("Error:", error);
        // Handle the error
      });
  };

  // Read the file as text
  reader.readAsText(file);//ArrayBuffer(file);
}
async function onSubmit(values) {
  if (values.document) {
    console.log(">>>>>>>>>>>> " + values.document.name);
    console.log(">>>>>>>>>>>> " + values.document.size);
    sendFileAsFormData(values.document);
  }
  document.getElementById("infile").value = null;
  document.getElementById("site").value = null;
}
</script>

<template>
  <div class="d-flex align-items-center justify-content-center w-100">
    <div class="card w-50 h-40">
      <h4 class="card-header">Index Image</h4>
      <div class="card-body">
        <Form
          @submit="onSubmit"
          :validation-schema="schema"
          id="myForm"
          v-slot="{ isSubmitting }"
        >
          <div class="form-group">
            <Field
              name="document"
              type="file"
              class="form-control choose-file-button"
              id="infile"
            />
          </div>
          <div class="form-group">
            <button class="btn btn-primary" :disabled="isSubmitting">
              <span
                v-show="isSubmitting"
                class="spinner-border spinner-border-sm mr-1"
              ></span>
              Submit
            </button>
            <p></p>
          </div>
        </Form>
        <div>
      </div>
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
