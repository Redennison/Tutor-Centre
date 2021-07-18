const fill_stars = (num) => {
    for (i=1; i<6; i++) {
        if (i <= num) {
            document.getElementById(`star-${i}`).checked = true;
        } else {
            document.getElementById(`star-${i}`).checked = false;
        }
    }
}