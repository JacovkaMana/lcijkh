import "./styles.css";

const RequestList = ({ data, center, setCenter }) => {
    return (
        <div className="RequestList">
            <table className="RequestList__table small-third-col">
                <thead>
                    <tr className="RequestList__header">
                        <th className="header__first">Наименование</th>
                        <th>Дата, время</th>
                        <th className="header__smallcol">Дефект</th>
                        <th className="header__last">Адрес</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map(rqst => {
                        return (
                            <tr
                                key={rqst.unique_id}
                                onClick={() =>
                                    setCenter([
                                        rqst.adress_id.latitude,
                                        rqst.adress_id.longitude
                                    ])
                                }
                                className={
                                    `RequestList__listitem 
                                ${rqst.anomaly ? 'item-red' : 'item-yellow'}`
                                }>
                                <td>{rqst.description}</td>
                                <td>{rqst.started_at.split('T').join(', ')}</td>
                                <td>{rqst.defect_id_id}</td>
                                <td>{rqst.adress_id.adress}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
        </div>
    )
}

export default RequestList