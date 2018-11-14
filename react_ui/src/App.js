import React, { Component } from 'react';
import TabularMenu from './components/TabularMenu'
import OverviewSegment from './components/OverviewSegment'
import TaskSegment from './components/TaskSegment'
import ZipModal from './components/ZipModal'

import 'semantic-ui-css/semantic.min.css'

class App extends Component {
    constructor(props) {
        super(props)
        this.state = {
            activeItem: 'zip overview',
            focusZip: null
        }
        this.clickTabHandler = this.clickTabHandler.bind(this)
        this.clickRowHandler = this.clickRowHandler.bind(this)
        this.unfocusZip = this.unfocusZip.bind(this)
    }

    clickTabHandler(e, props) {
        this.setState({ activeItem: props.name })
    }

    clickRowHandler(e, row) {
        this.setState({ focusZip: row.getData().zip_id})
    }

    unfocusZip(){
        this.setState({ focusZip: null })
    }

    render() {
        return (
            <div className="App">
                <TabularMenu
                    clickHandler={this.clickTabHandler}
                    activeItem={this.state.activeItem}
                />
                {this.state.activeItem==='zip overview'? <OverviewSegment clickRowHandler={this.clickRowHandler} />: null}
                {this.state.activeItem==='task overview'? <TaskSegment />: null}
                <ZipModal zipId={this.state.focusZip} unfocusZip={ this.unfocusZip }/>
            </div>
        );
    }
}

export default App;
