
function MoistureCardd({ moist_value }) {
    return (
        <div className="moistcard">
          <div className="card-head">Moisture</div>
          <div className="percentvalue">{moist_value}%</div>
        </div>
    )
}

export default MoistureCardd