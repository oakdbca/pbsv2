<template lang="html">
    <div>
        <div class="form-group">
            <ckeditor
                :id="id"
                v-model="detailsText"
                :editor="editor"
                :config="editor.defaultConfig"
                :name="name"
                :required="isRequired"
                :disabled="readonly"
                :read-only="readonly"
            />
        </div>
    </div>
</template>

<script>
import Editor from "./ckeditor.js";

export default {
    name: "RichText",
    props: {
        id: {
            type: String,
            required: true,
        },
        name: {
            type: String,
            required: true,
        },
        label: {
            type: String,
            required: true,
        },
        proposalData: {
            type: String,
            required: true,
        },
        isRequired: {
            type: Boolean,
        },
        readonly: {
            type: Boolean,
        },
        canViewRichtextSrc: {
            type: Boolean,
        },
        placeholderText: {
            type: String,
            default: "",
        },
    },
    emits: ["textChanged"],
    data() {
        let remove_buttons = "";

        if (!this.canViewRichtextSrc) {
            // eslint-disable-next-line no-unused-vars, @typescript-eslint/no-unused-vars
            remove_buttons = "Source,About";
        }
        return {
            detailsText: "",
            editor: Editor,
        };
    },
    watch: {
        detailsText: function () {
            // Parent component can subscribe this event in order to update text
            if (this.proposalData == this.detailsText) {
                // Only emit if the text was changed through input, not through the parent component
                return;
            }
            this.$emit("textChanged", this.detailsText);
        },
    },
    created: function () {
        if (this.proposalData) {
            this.detailsText = this.proposalData;
        }
        this.editor.defaultConfig["placeholder"] = this.placeholderText;
    },
    methods: {
        focus() {
            console.log("focus rich text");
            this.$nextTick(() => {
                $(".ck-editor__editable").focus();
            });
        },
    },
};
</script>
