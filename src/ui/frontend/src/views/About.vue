<script setup>
import { Form, Field } from "vee-validate";
import * as Yup from "yup";
import axios from "axios";

function sendFileAsFormData(file) {
  // Create a new FormData object
  var formData = new FormData();

  // Read the file content using FileReader
  var reader = new FileReader();
  reader.onload = function (event) {
    var fileContent = event.target.result;

    // Append the file and file content to the FormData object
    formData.append("file", file);
    formData.append("fileContent", fileContent);

    // Create the Fetch API request
    var request = new Request("http://localhost:8000/indexinventory", {
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
  reader.readAsArrayBuffer(file);
}
async function onSubmit(values) {
  if (values.website) {
    console.log(">>>>>>>>>>>> " + encodeURI(values.website));
    const params = new URLSearchParams();
    params.append("pageurl", values.website);
    axios
      .post("http://localhost:8000/indeximage" + params.toString())
      .then((response) => {
        console.log(">>>>>>>>>>>> URL posted for indexing successfully");
      })
      .catch((error) => {});
  } else if (values.document) {
    console.log(">>>>>>>>>>>> " + values.document[0].name);
    console.log(">>>>>>>>>>>> " + values.document[0].size);
    sendFileAsFormData(values.document[0]);
  }
  document.getElementById("infile").value = null;
  document.getElementById("site").value = null;
}
</script>

<template>
  <div class="d-flex align-items-center justify-content-center w-100">
    <h6 style="color: #fff">
      Image Search Powered by Generative AI
    </h6>
  </div>
</template>
