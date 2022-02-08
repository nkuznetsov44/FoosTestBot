import React from "react";
import DataGrid, { Column, Selection } from 'devextreme-react/data-grid';

export const TestSessionsTable = (props) => {
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
      <Column dataField="score" />
    </DataGrid>
  );
};