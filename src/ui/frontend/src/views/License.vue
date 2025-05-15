<script setup>
// Static HTML content without bullets (but using <ul><li> for structure)
const licenseHtml = `
  <b>Licenses</b>
  <br><br>
  CLIP (Contrastive Language-Image Pre-training)
  <ul>
    <li>
      <a href='https://pypi.org/project/open-clip-torch/' target="_blank">https://pypi.org/project/open-clip-torch/</a>
    </li>
    <li>
      <a href='https://github.com/mlfoundations/open_clip/blob/main/LICENSE' target="_blank">https://github.com/mlfoundations/open_clip/blob/main/LICENSE</a>
    </li>
  </ul>
  Langchain
  <ul>
    <li>
      <a href='https://pypi.org/project/langchain/' target="_blank">https://pypi.org/project/langchain/</a>
    </li>
    <li>
      <a href='https://github.com/langchain-ai/langchain/blob/master/LICENSE' target="_blank">https://github.com/langchain-ai/langchain/blob/master/LICENSE</a>
    </li>
  </ul>
  Transformers
  <ul>
    <li>
      <a href='https://pypi.org/project/transformers/' target="_blank">https://pypi.org/project/transformers/</a>
    </li>
    <li>
      <a href='https://github.com/huggingface/transformers/blob/main/LICENSE' target="_blank">https://github.com/huggingface/transformers/blob/main/LICENSE</a>
    </li>
  </ul>
  Milvus
  <ul>
    <li>
      <a href='https://milvus.io/docs/product_faq.md#How-much-does-Milvus-cost' target="_blank">https://milvus.io/docs/product_faq.md#How-much-does-Milvus-cost</a>
    </li>
  </ul>
  PyMilvus
  <ul>
    <li>
      <a href='https://pypi.org/project/pymilvus/' target="_blank">https://pypi.org/project/pymilvus/</a>
    </li>
    <li>
      <a href='https://github.com/milvus-io/pymilvus/blob/master/LICENSE' target="_blank">https://github.com/milvus-io/pymilvus/blob/master/LICENSE</a>
    </li>
  </ul>
`;
</script>

<template>
  <div
    v-html="licenseHtml"
    class="license-content p-5 anchor"
  ></div>
</template>

<style scoped>
.license-content {
  color: white;
  text-align: left;
  margin-top: 50px;
  margin-left: 20%;
}
.license-content ul {
  margin: 0 0 16px 40px;  /* Indent the list */
  padding-left: 0;
  list-style: none;        /* Remove bullets */
}
.license-content li {
  margin-bottom: 4px;
}
</style>
