import React, { Component } from 'react';
import { Menu } from 'semantic-ui-react';
import logo from '../assets/logo/logo.png' 

class TabularMenu extends Component {

    render() {
        return (
            <Menu tabular attached='top' >
                <Menu.Item>
                    <img src={logo} className='logo' alt='Zipline'/>
                </Menu.Item>
                <Menu.Item
                    name='zip overview'
                    active={this.props.activeItem === 'zip overview'}
                    onClick={this.props.clickHandler}
                />
                <Menu.Item
                    name='task overview'
                    active={this.props.activeItem === 'task overview'}
                    onClick={this.props.clickHandler}
                />
            </Menu>
        )
    }
}

export default TabularMenu;