/** @odoo-module **/
import { Component, useState } from '@odoo/owl';

class MyComponent extends Component {
    constructor() {
        console.log('test');
        super(...arguments);
        this.state = useState({
            message: "Hello from OWL Component!",
        });
    }

    render() {
        return (
            <div>
                <h2>{this.state.message}</h2>
                <button onClick={() => this.changeMessage()}>Click me</button>
            </div>
        );
    }

    changeMessage() {
        this.state.message = "You've clicked the button!";
    }
}

export default MyComponent;
