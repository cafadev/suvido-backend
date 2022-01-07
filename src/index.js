import Alpine from 'alpinejs'


import { videoComponent } from './js/main'
import { loginComponent } from './js/login'

import './styles/main.css'

Alpine.data('app', () => ({
  ...videoComponent,
  ...loginComponent
}))

Alpine.start()
