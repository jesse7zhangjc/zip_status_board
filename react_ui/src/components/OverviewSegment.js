import React, { Component } from 'react';
import { Segment } from 'semantic-ui-react';
import { ReactTabulator } from 'react-tabulator';
import 'react-tabulator/lib/css/semantic-ui/tabulator_semantic-ui.min.css';
import Service from '../services/fetch';

class OverviewSegment extends Component {
    constructor(props) {
        super(props)
        this.state = {'data': []}
        this.apiService = new Service()
        this.refreshData = this.refreshData.bind(this)

        this.columns = [
            { title: 'ID', field: 'zip_id', width: 80 },
            { title: 'Zip Name', field: 'zip_name', width: 150 },
            { title: 'Tasks Done', field: 'task_done', width: 150, formatter: 'tickCross' },
            { title: 'Not Blocked', field: 'non_blocking', width: 150, formatter: 'tickCross' },
            { title: 'Status', field: 'health', formatter: 'lookup', formatterParams: {
                0: 'Do NOT fly',
                1: 'Can fly with remaining tasks',
                2: 'OK to fly',
            }}
        ]
    }

    async refreshData() {
        const response = await this.apiService.get('zips')
        if (response.status === 200) {
            this.setState({ data: response.data })
        }
    }

    componentDidMount() {
        this.refreshData()
    }

    componentWillReceiveProps() {
        this.refreshData()
    }

    render() {
        return (
            <Segment className='overview' attached='bottom'>
                <ReactTabulator
                    className='overview-table'
                    data={this.state.data}
                    columns={this.columns}
                    layout='fitData'
                    selectableRangeMode="click"
                    selectable
                    rowClick={this.props.clickRowHandler}
                />
            </Segment>
        )
    }
}

export default OverviewSegment;