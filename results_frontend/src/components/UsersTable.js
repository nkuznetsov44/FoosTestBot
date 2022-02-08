import React from "react";
import DataGrid, { Column, Selection } from 'devextreme-react/data-grid';

export const UsersTable = (props) => {
  return (
    <DataGrid
      dataSource={props.users}
      showBorders={true}
      hoverStateEnabled={true}
      columnAutoWidth={true}
      keyExpr="user_id"
      onSelectionChanged={props.onUserSelectionChanged}
    >
      <Selection mode="single" />
      <Column dataField="username" />
      <Column dataField="first_name" />
      <Column dataField="last_name" />
    </DataGrid>
  );
};