export const loginComponent = () => ({
  dialog: false,
  form: {
    first_name: '',
    email: '',
    password: ''
  },

  openDialog() {
    this.dialog = true
  },

  closeDialog() {
    this.dialog = false
  }
})
