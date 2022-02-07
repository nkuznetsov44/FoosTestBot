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
  }, [selectedUserId, answersNeedUpdate]);

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
  };

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
          <Column dataField="question" width="5%" alignment="right" caption="#" allowEditing={false} />
          <Column dataField="question_text" width="50%" alignment="left" caption="Вопрос" allowEditing={false} />
          <Column dataField="answer" width="5%" alignment="left" caption="Ответ" allowEditing={false} />
          <Column dataField="correct_answer_index" width="5%" alignment="left" caption="Номер верного ответа" allowEditing={false} />
          <Column dataField="correct_answer" width="20%" alignment="left" caption="Текст верного ответа" allowEditing={false} />
          <Column dataField="is_correct" width="5%" alignment="center" caption="Ответ верный?" allowEditing={true} />
          <Column dataField="answer_time" width="10%" alignment="left" caption="Время" allowEditing={false} />
        </DataGrid>
      </section>
    </div>
  );
}

export default App;
