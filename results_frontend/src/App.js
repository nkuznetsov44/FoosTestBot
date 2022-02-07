import 'devextreme/dist/css/dx.common.css';
import 'devextreme/dist/css/dx.light.css';
import './App.css';
import React from "react";
import axios from "axios";
import * as _ from 'lodash';
import 'devextreme/dist/css/dx.light.css';
import DataGrid, { Column, Selection, Scrolling, Editing } from 'devextreme-react/data-grid';

function App() {
  const [users, setUsers] = React.useState([]);
  const [selectedUserId, setSelectedUserId] = React.useState(null);
  const [testSessions, setTestSessions] = React.useState([]);
  const [selectedTestSessionId, setSelectedTestSessionId] = React.useState(null);
  const [answers, setAnswers] = React.useState(null);

  React.useEffect(() => {
    axios.get('/api/users').then((response) => {
      setUsers(response.data);
    });
  }, []);

  React.useEffect(() => {
    if (!_.isNull(selectedUserId)) {
      axios.get(`/api/testSessions/${selectedUserId}`).then((response) => {
        setTestSessions(response.data);
      });
    }
  }, [selectedUserId]);

  React.useEffect(() => {
    if (!_.isNull(selectedUserId)) {
      axios.get(`/api/answers/${selectedTestSessionId}`).then((response) => {
        setAnswers(response.data);
      });
    }
  }, [selectedTestSessionId]);

  const onUserSelectionChanged = ({ selectedRowsData }) => {
    const selectedUser = selectedRowsData[0];
    if (!_.isNull(selectedUser)) {
      setSelectedUserId(selectedUser.user_id);
    }
  };

  const onTestSessionSelectionChanged = ({ selectedRowsData }) => {
    const selectedTestSession = selectedRowsData[0];
    if (!_.isNull(selectedTestSession)) {
      setSelectedTestSessionId(selectedTestSession.id);
    }
  };

  const onSaved = ({ changes }) => {
    const data = changes.map((change) => change.data);
    axios.post(
      '/api/answers/changes', data
    ).then((response) => {
      console.log(response);
    });
  };

  /*const selectedUserScoreElement = () => {
    if (!_.isNull(selectedUserId) && !_.isNull(answers)) {
      const score = selectedUserAnswers
        .map((answer) => answer.is_correct)
        .reduce((v1, v2) => v1 + v2);
      const totalScore = selectedUserAnswers
        .map((answer) => !_.isNull(answer.is_correct))
        .reduce((v1, v2) => v1 + v2);
      const allAnswersAreChecked = selectedUserAnswers
        .map((answer) => !_.isNull(answer.is_correct))
        .reduce((v1, v2) => v1 && v2);
      let className = "unchecked";
      if (allAnswersAreChecked) {
        if (score >= 23) className = "checked-passed";
        else className = "checked-failed"
      }
      return (
        <h2 className={className}>Score: {score}/{totalScore}</h2>
      )
    }
    return <div />;
  };*/

  return (
    <div className="App">
      <h1>Результаты теста арбитра ITSF</h1>
      <section className="users">
        <DataGrid
          dataSource={users}
          showBorders={true}
          hoverStateEnabled={true}
          columnAutoWidth={true}
          keyExpr="user_id"
          onSelectionChanged={onUserSelectionChanged}
        >
          <Selection mode="single" />
          <Column dataField="username" />
          <Column dataField="first_name" />
          <Column dataField="last_name" />
        </DataGrid>
      </section>
      <section className="testSessions">
        <DataGrid
          dataSource={testSessions}
          showBorders={true}
          hoverStateEnabled={true}
          columnAutoWidth={true}
          keyExpr="id"
          onSelectionChanged={onTestSessionSelectionChanged}
        >
          <Selection mode="single" />
          <Column dataField="id" />
          <Column dataField="start_time" />
          <Column dataField="end_time" />
          <Column dataField="score" />
        </DataGrid>
      </section>
      <section className="answers">
        <DataGrid
          dataSource={answers}
          showBorders={true}
          hoverStateEnabled={true}
          wordWrapEnabled={true}
          rowAlternationEnabled={true}
          onSaved={onSaved}
        >
          <Scrolling mode="virtual" />
          <Editing
            mode="batch"
            allowUpdating={true}
            allowAdding={false}
            allowDeleting={false} />
          <Column dataField="question.code" width="5%" alignment="right" caption="#" allowEditing={false} />
          <Column dataField="question.text" width="50%" alignment="left" caption="Вопрос" allowEditing={false} />
          <Column dataField="answer" width="5%" alignment="left" caption="Ответ" allowEditing={false} />
          <Column dataField="question.correct_answer_index" width="5%" alignment="left" caption="Номер верного ответа" allowEditing={false} />
          <Column dataField="question.correct_answer_text" width="20%" alignment="left" caption="Текст верного ответа" allowEditing={false} />
          <Column dataField="is_correct" width="5%" alignment="center" caption="Ответ верный?" allowEditing={true} />
        </DataGrid>
      </section>
    </div>
  );
}

export default App;
