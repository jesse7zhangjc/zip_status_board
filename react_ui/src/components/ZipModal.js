import React, { Component } from 'react';
import { Modal, Button, Grid, Header, Segment } from 'semantic-ui-react';

import ZipStatus from './ZipStatus'
import NewTaskSegment from './NewTaskSegment'
import TaskHistory from './TaskHistory'
import Service from '../services/fetch';

class ZipModal extends Component {
    constructor(props){
        super(props)
        this.state = {
            statusData: {},
            taskHistoryData: []
        }
        this.apiService = new Service()
        this.refreshData = this.refreshData.bind(this)
        this.cellEditedHandler = this.cellEditedHandler.bind(this)
    }

    async refreshData(zipId) {
        if (zipId) {
            const zipObj = await this.apiService.get(`zips/${zipId}`)
            if (zipObj.status === 200) {
                this.setState({
                    statusData: zipObj.data.status,
                    taskHistoryData: zipObj.data.task_history
                })
            }
        }
    }

    async cellEditedHandler(cell) {
        let body = {}
        body.resolve = cell.getValue()
        body.task_ids = [cell.getData().task_id]
        const resp = await this.apiService.put('tasks', body)
        if (resp.status === 200) {
            this.refreshData(this.props.zipId)
        }
    }

    componentDidMount() {
        this.refreshData(this.props.zipId)
    }

    componentWillReceiveProps(nextProps) {
        if (nextProps.zipId) {
        this.refreshData(nextProps.zipId)
        }
    }

    render() {
        if (this.props.zipId) {
            return (
                <Modal open={this.props.zipId > 0} size='large'>
                    <Modal.Header content={this.state.statusData.zip_name} />
                    <Modal.Content>

                        <Grid columns={2} textAlign='center' verticalAlign='top'>
                            <Grid.Row>

                                <Grid.Column width={6}>
                                    {this.state.statusData? <ZipStatus statusData={this.state.statusData} />:null}
                                </Grid.Column>

                                <Grid.Column width={10}>
                                    <Segment>
                                        <Header as= 'h3' content='Add New Maintenance Tasks'/>
                                        <NewTaskSegment zipId={this.props.zipId} refreshData={this.refreshData}/>
                                    </Segment>
                                    <Segment>
                                        <Header as='h3' content='Maintenance Tasks'/>
                                        {this.state.taskHistoryData? <TaskHistory taskHistoryData={this.state.taskHistoryData} editedHandler={this.cellEditedHandler} />:null}
                                    </Segment>
                                </Grid.Column>

                            </Grid.Row>
                        </Grid>

                    </Modal.Content>
                    <Modal.Actions>
                        <Button
                            content='Close'
                            onClick={() => {
                                this.props.unfocusZip()
                                this.setState({
                                    statusData: {},
                                    taskHistoryData: []
                                })
                            }}
                        />
                    </Modal.Actions>
                </Modal>
            )
        }
        else {
            return null
        }
    }
}

export default ZipModal;