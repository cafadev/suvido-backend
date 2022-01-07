import axios from 'axios'

const SERVER = window.location.hostname === 'localhost' ? 'http://localhost:9000/api' : ''

axios.defaults.baseURL = SERVER

export default axios