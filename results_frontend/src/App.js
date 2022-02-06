import 'devextreme/dist/css/dx.common.css';
import 'devextreme/dist/css/dx.light.css';
import './App.css';
import React from "react";
import axios from "axios";
import * as _ from 'lodash';
import 'devextreme/dist/css/dx.light.css';
import Button from 'devextreme-react/button';
import DataGrid, { Column, Selection, Scrolling, Editing } from 'devextreme-react/data-grid';

function App() {
  const [users, setUsers] = React.useState([]);
  const [selectedUserId, setSelectedUserId] = React.useState(null);
  const [selectedUserAnswers, setSelectedUserAnswers] = React.useState(null);
  const [answersNeedUpdate, setAnswersNeedUpdate] = React.useState(false);

  React.useEffect(() => {
    axios.get('/api/users').then((response) => {
      setUsers(response.data);
    });
  }, []);

  React.useEffect(() => {
    if (answersNeedUpdate) {
      if (!_.isNull(selectedUserId)) {
        axios.get(`/api/answers/${selectedUserId}`).then((response) => {
          setSelectedUserAnswers(response.data);
        });
      }
      setAnswersNeedUpdate(false);
    }
  }, [answersNeedUpdate]);

  React.useEffect(() => {
    if (!_.isNull(selectedUserId)) {
      setAnswersNeedUpdate(true);
    }
  }, [selectedUserId]);

  const onSelectionChanged = ({ selectedRowsData }) => {
    const selectedUser = selectedRowsData[0];
    if (!_.isNull(selectedUser)) {
      setSelectedUserId(selectedUser.user_id);
    }
  };

  const onSaved = ({ changes }) => {
    const data = changes.map((change) => change.data);
    axios.post(
      '/api/answers/changes', data
    ).then((response) => {
      setAnswersNeedUpdate(true);
    });
  };

  const selectedUserScoreElement = () => {
    if (!_.isNull(selectedUserId) && !_.isNull(selectedUserAnswers)) {
      const score = selectedUserAnswers
        .map((answer) => answer.is_correct)
        .reduce((v1, v2) => v1 + v2);
      const totalScore = selectedUserAnswers
        .map((answer) => !_.isNull(answer.is_correct))
        .reduce((v1, v2) => v1 + v2);
      const allAnswersAreChecked = selectedUserAnswers
        .map((answer) => !_.isNull(answer.is_correct))
        .reduce((v1, v2) => v1 && v2);
      return (
        <h2 className={allAnswersAreChecked ? "checked" : "unchecked"}>Score: {score}/{totalScore}</h2>
      )
    }
    return <div />;
  };

  return (
    <div className="App">
      <h1>Foos test results</h1>
      <section className="users">
        <DataGrid
          dataSource={users}
          showBorders={true}
          hoverStateEnabled={true}
          columnAutoWidth={true}
          keyExpr="user_id"
          onSelectionChanged={onSelectionChanged}
        >
          <Selection mode="single" />
          <Column dataField="username" />
          <Column dataField="first_name" />
          <Column dataField="last_name" />
        </DataGrid>
      </section>
      <section className="score">
        {selectedUserScoreElement()}
      </section>
      <section className="answers">
        <DataGrid
          dataSource={selectedUserAnswers}
          showBorders={true}
          hoverStateEnabled={true}
          columnAutoWidth={true}
          rowAlternationEnabled={true}
          onSaved={onSaved}
        >
          <Scrolling mode="virtual" />
          <Editing
            mode="batch"
            allowUpdating={true}
            allowAdding={false}
            allowDeleting={false} />
          <Column dataField="question" allowEditing={false} />
          <Column dataField="answer" allowEditing={false} />
          <Column dataField="is_correct" allowEditing={true} />
          <Column dataField="answer_time" allowEditing={false} />
        </DataGrid>
      </section>
    </div>
  );
}

export default App;
