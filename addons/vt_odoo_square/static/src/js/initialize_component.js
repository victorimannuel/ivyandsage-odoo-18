/** @odoo-module **/

import { App } from '@odoo/owl';
import MyComponent from './my_component';

// Wait for the document to be ready
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('my-component-container');
    if (container) {
        const app = new App(MyComponent);
        app.mount(container);  // Mount the OWL component to the container
    }
});
