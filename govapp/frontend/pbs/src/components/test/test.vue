<template>
    <div id="testvue" class="container">
            This is a test page!!
    </div>
</template>

<script>


export default {
    name: 'TestVue',
    components: {    
    },
    data: function () {

    },
    computed: {

    },
    mounted: async function () {
       console.log("test template loaded");
    },
};
</script>