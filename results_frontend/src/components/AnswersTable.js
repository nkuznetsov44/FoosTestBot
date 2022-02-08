import React from "react";
import axios from "axios";
import DataGrid, { Column, Editing, Paging } from 'devextreme-react/data-grid';
import notify from 'devextreme/ui/notify';

export const AnswersTable = (props) => {

  const onSaved = ({ changes }) => {
    const data = changes.map((change) => change.data);
    axios.post(
      `/api/answers/checked/${props.testSessionId}`, data
    ).then((response) => {
      notify('Ответы сохранены', 'success', 2000);
      props.onAnswersSaved();
    }).catch((error) => {
      console.log(error);
      notify('Ошибка сохранения ответов', 'error', 2000);
    });
  };

  return (
    <DataGrid
      dataSource={props.answers}
      showBorders={true}
      hoverStateEnabled={true}
      wordWrapEnabled={true}
      rowAlternationEnabled={true}
      onSaved={onSaved}
    >
      <Paging defaultPageSize={30} />
      <Editing
        mode="batch"
        allowUpdating={true}
        allowAdding={false}
        allowDeleting={false}
      />
      <Column
        dataField="question.code"
        width="5%"
        alignment="right"
        caption="#"
        allowEditing={false}
      />
      <Column
        dataField="question.text"
        width="60%"
        alignment="left"
        caption="Вопрос"
        allowEditing={false}
      />
      <Column
        dataField="answer"
        width="5%"
        alignment="left"
        caption="Ответ"
        allowEditing={false}
      />
      <Column
        dataField="question.correct_answer_index"
        width="5%"
        alignment="left"
        caption="Номер верного ответа"
        allowEditing={false}
      />
      <Column
        dataField="question.correct_answer_text"
        width="20%"
        alignment="left"
        caption="Текст верного ответа"
        allowEditing={false}
      />
      <Column
        dataField="is_correct"
        width="5%"
        alignment="center"
        caption="Ответ верный?"
        allowEditing={true}
      />
    </DataGrid>
  );
};