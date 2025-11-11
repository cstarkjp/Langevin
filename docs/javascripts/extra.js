"use strict";

window.addEventListener("DOMContentLoaded", _ => {
    myModifyViewPageButtonToBlob();
});

const myModifyViewPageButtonToBlob = () => {
    for (const anchor of document.querySelectorAll("a.md-content__button")) {
        anchor.href = anchor.href.replace("/raw/main/", "/blob/main/");
    }
};