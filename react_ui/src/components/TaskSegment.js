import React, { Component } from 'react';
import { Segment, Button } from 'semantic-ui-react';
import { ReactTabulator } from 'react-tabulator';
import 'react-tabulator/lib/css/semantic-ui/tabulator_semantic-ui.min.css';
import Service from '../services/fetch';


class TaskSegment extends Component {
    constructor(props) {
        super(props)
        this.state = {'data': [], selected: []}
        this.apiService = new Service()
        this.refreshData = this.refreshData.bind(this)
        this.cellEditedHandler = this.cellEditedHandler.bind(this)
        this.implementAllHandler = this.implementAllHandler.bind(this)
        this.filterHandler = this.filterHandler.bind(this)
        this.columns = [
            { title: 'Task ID', field: 'task_id', width: 100 },
            { title: 'Resolved?', field: 'resolved', formatter: 'tickCross', width: 150, editor:true },
            { title: 'Non-Blocking', field: 'non_blocking', formatter: 'tickCross', width: 150 },
            { title: 'Prob ID', field: 'problem_id', width: 150, headerFilter: true },
            { title: 'Problem', field: 'problem_name' },
            { title: 'Zip ID', field: 'zip_id', width: 150 },
            { title: 'Zip Name', field: 'zip_name', width: 150 }
        ]
    }

    ref = null

    async refreshData() {
        const response = await this.apiService.get('tasks')
        if (response.status === 200) {
            this.setState({ data: response.data })
        }
    }

    async cellEditedHandler(cell) {
        let body = {}
        body.resolve = cell.getValue()
        body.task_ids = [cell.getData().task_id]
        const resp = await this.apiService.put('tasks', body)
        if (resp.status !== 200) {
            this.refreshData()
        }
    }

    filterHandler(filters, rows) {
        let selectedTaskIds = []
        rows.forEach((x) => {
            selectedTaskIds.push(x.getData().task_id)
        })
        this.setState({selected: selectedTaskIds})
    }

    async implementAllHandler() {
        let body = {}
        body.resolve = 1
        body.task_ids = this.state.selected
        const resp = await this.apiService.put('tasks', body)
        if (resp.status === 200) {
            this.refreshData()
        }
    }
        

    componentDidMount() {
        this.refreshData()
    }

    componentWillReceiveProps() {
        this.refreshData()
    }

    shouldComponentUpdate(nextProps, nextState) {
      return this.state.data !== nextState.data;
    }


    render() {
        return (
            <Segment className='task' attached='bottom'>
                <div>
                    <Button content='Implement All' positive onClick={this.implementAllHandler}/>
                </div>
                <ReactTabulator
                    ref={ref => (this.ref = ref)}
                    className='task-table'
                    data={this.state.data}
                    columns={this.columns}
                    layout='fitData'
                    cellEdited={this.cellEditedHandler}
                    dataFiltered={this.filterHandler}
                />
            </Segment>
            
        )
    }
}

export default TaskSegment;