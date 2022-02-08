import 'devextreme/dist/css/dx.common.css';
import 'devextreme/dist/css/dx.light.css';
import './App.css';
import React from "react";
import axios from "axios";
import * as _ from 'lodash';
import { UsersTable} from './components/UsersTable';
import { TestSessionsTable } from './components/TestSessionsTable';
import { AnswersTable } from './components/AnswersTable';

const App = () => {
  const [users, setUsers] = React.useState([]);
  const [selectedUserId, setSelectedUserId] = React.useState(null);
  const [testSessions, setTestSessions] = React.useState([]);
  const [selectedTestSessionId, setSelectedTestSessionId] = React.useState(null);
  const [testSessionsNeedUpdate, setTestSessionsNeedUpdate] = React.useState(false);
  const [answers, setAnswers] = React.useState(null);

  React.useEffect(() => {
    axios.get('/api/users').then((response) => {
      setUsers(response.data);
    });
  }, []);

  React.useEffect(() => {
    if (!_.isNull(selectedUserId) && testSessionsNeedUpdate) {
      axios.get(`/api/testSessions/${selectedUserId}`).then((response) => {
        setTestSessions(response.data);
      });
      setTestSessionsNeedUpdate(false);
    }
  }, [selectedUserId, testSessionsNeedUpdate]);

  React.useEffect(() => {
    if (!_.isNull(selectedTestSessionId)) {
      axios.get(`/api/answers/${selectedTestSessionId}`).then((response) => {
        setAnswers(response.data);
      });
    }
  }, [selectedTestSessionId]);

  const onUserSelectionChanged = ({ selectedRowsData }) => {
    const selectedUser = selectedRowsData[0];
    if (!_.isNull(selectedUser)) {
      setSelectedUserId(selectedUser.user_id);
      setTestSessionsNeedUpdate(true);
    }
  };

  const onTestSessionSelectionChanged = ({ selectedRowsData }) => {
    const selectedTestSession = selectedRowsData[0];
    if (!_.isNull(selectedTestSession)) {
      setSelectedTestSessionId(selectedTestSession.id);
    }
  };

  const onAnswersSaved = () => {
    setTestSessionsNeedUpdate(true);
  };

  return (
    <div className="App">
      <h1>Результаты теста арбитра ITSF</h1>
      <section className="users">
        <UsersTable
          users={users}
          onUserSelectionChanged={onUserSelectionChanged}
        />
      </section>
      <section className="testSessions">
        <TestSessionsTable
          testSessions={testSessions}
          onTestSessionSelectionChanged={onTestSessionSelectionChanged}
        />
      </section>
      <section className="answers">
        <AnswersTable
          testSessionId={selectedTestSessionId}
          answers={answers}
          onAnswersSaved={onAnswersSaved}
        />
      </section>
    </div>
  );
};

export default App;