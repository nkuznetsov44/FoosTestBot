import React from "react";
import axios from "axios";
import DataGrid, { Column, Selection, Editing, Scrolling } from 'devextreme-react/data-grid';

export const AnswersTable = (props) => {

  const onSaved = ({ changes }) => {
    const data = changes.map((change) => change.data);
    axios.post(
      '/api/answers/changes', data
    ).then((response) => {
      console.log(response);
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
      <Scrolling mode="virtual" />
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
        width="50%"
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