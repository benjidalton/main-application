
// /**
//  * plugins/vuetify.js
//  *
//  * Framework documentation: https://vuetifyjs.com`
//  */

// // Styles
// 
// import 'vuetify/styles';

// // Composables
// import { createVuetify } from 'vuetify';

// // https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
// export default createVuetify({
//   theme: {
//     themes: {
//       light: {
//         colors: {
//           primary: '#145DA0',
//           secondary: '#75787B',
//           success: '#198754',
//           // success: '#43B02A',
//           info: '#1e72fe',
//           danger: '#DA291C',
//           warning: '#ffc107',
//           lightfill: '#f1f3f5',
//         },
//       },
//       dark: {
//         colors: {
//           primary: '#145DA0',
//           secondary: '#75787B',
//           success: '#198754',
//           info: '#1e72fe',
//           danger: '801b13',
//           warning: '#ffc107',
//         },
//       },
//     },
//   },
// });

// plugins/vuetify.js
import '@mdi/font/css/materialdesignicons.css';
import { createVuetify } from 'vuetify';
import 'vuetify/styles'; // Import Vuetify styles

const vuetify = createVuetify(); // Vuetify instance

export default vuetify;