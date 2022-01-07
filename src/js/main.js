import axios from './axios'

export const videoComponent = () => ({
  isDropdownVisible: false,
  loading: false,
  ranking: [],

  video: {
    url: 'https://www.youtube.com/watch?v=s6dMWzZKjTs',
    static_url: '',
    title: '',
    thumbnail: '',
    formats: []
  },

  clearVideo() {
    Object.assign(this.video, {
      url: 'https://www.youtube.com/watch?v=tYaqe-J6UR8',
      title: '',
      thumbnail: '',
      formats: []
    })
  },

  searchVideo() {
    if (!this.video.url) return

    this.loading = true

    const params = { url: this.video.url }

    axios.get('videos/', { params }).then(response => {
      Object.assign(this.video, response.data)
    })
    .finally(() => this.loading = false)

    this.clearVideo()
  },
  
  openDropdown() {
    this.isDropdownVisible = true
  },
  
  closeDropdown() {
    this.isDropdownVisible = false
  },
  
  toggle() {
    this.isDropdownVisible = ! this.isDropdownVisible
  },

  downloadResource(format=null) {
    this.closeDropdown()

    if (!this.video.formats.length) return
    
    this.loading = true

    const _format = format.url ? format : this.video.formats[0]

    axios({
      url: 'videos/',
      method: 'POST',
      responseType: 'blob',
      data: { url: _format.url, title: this.video.title, video_url: this.video.static_url },
      onDownloadProgress(progress) {
        console.log(progress)
      }
    })
    .then((response) => {
      const filename = `video.${_format.ext}`

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');

      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
    }).finally(() => this.loading = false);
  }
})
