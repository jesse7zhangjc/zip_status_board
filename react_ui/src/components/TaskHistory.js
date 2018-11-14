import React, { Component } from 'react';
import { Grid } from 'semantic-ui-react';
import { ReactTabulator } from 'react-tabulator';
import 'react-tabulator/lib/css/semantic-ui/tabulator_semantic-ui.min.css';

class TaskHistory extends Component {
    constructor(props) {
        super(props)
        this.columns = [
            { title: 'Task ID', field: 'task_id', width: 100 },
            { title: 'Resolved?', field: 'resolved', width: 150, formatter: 'tickCross', editor: true },
            { title: 'Not Blocking?', field: 'non_blocking', width: 150, formatter: 'tickCross' },
            { title: 'Problem', field: 'problem_name'},
        ]
    }

    render() {
        return(
                <Grid textAlign='center' verticalAlign='middle'>
                    <Grid.Row>
                        <ReactTabulator
                            className='task-hist-table'
                            data={this.props.taskHistoryData}
                            columns={this.columns}
                            layout='fitData'
                            cellEdited={this.props.editedHandler}
                        />
                    </Grid.Row>
                </Grid>
        )
    }
}

export default TaskHistory;