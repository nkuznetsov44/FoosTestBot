import './TestSessionTable.css';
import React from "react";
import DataGrid, { Column, Selection } from 'devextreme-react/data-grid';

export const TestSessionsTable = (props) => {

  const scoreCellRender = ({ data }) => {
    let className = "score unchecked";
    if (data.is_checked) {
      if (data.score >= 23) {
        className = "score passed";
      } else {
        className = "score failed";
      }
    }
    return <div className={className}>{data.score}</div>
  };

  return (
    <DataGrid
      dataSource={props.testSessions}
      showBorders={true}
      hoverStateEnabled={true}
      columnAutoWidth={true}
      keyExpr="id"
      onSelectionChanged={props.onTestSessionSelectionChanged}
    >
      <Selection mode="single" />
      <Column dataField="id" />
      <Column dataField="start_time" />
      <Column dataField="end_time" />
      <Column dataField="score" cellRender={scoreCellRender} />
    </DataGrid>
  );
};