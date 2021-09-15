package banana.co;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.android.volley.RequestQueue;
import com.android.volley.toolbox.Volley;

import org.altbeacon.beacon.Beacon;

import java.util.ArrayList;
import java.util.List;

public class BeaconsAdapter extends RecyclerView.Adapter<BeaconsAdapter.BeaconViewHoldrer>{
    private List<Beacon> beaconsList= new ArrayList<Beacon>();
    Context context;
    ILoadMore loadMore;

    public BeaconsAdapter(List<Beacon> beaconsList, Context context) {
        this.beaconsList = beaconsList;
        this.context = context;

    }

    public void setLoadMore(ILoadMore loadMore) {
        this.loadMore = loadMore;
    }

    @NonNull
    @Override
    public BeaconViewHoldrer onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        LayoutInflater inflater = LayoutInflater.from(context);
        View view = inflater.inflate(R.layout.list_row, parent, false);

        return new BeaconViewHoldrer(view);
    }

    @Override
    public void onBindViewHolder(@NonNull BeaconViewHoldrer holder, int position) {
        holder.textName.setText(beaconsList.get(position).getId1().toString());
        holder.textDistance.setText(String.valueOf(beaconsList.get(position).getDistance()) +" meters");

        // Poslati Rest request
        //RequestQueue requestQueue= Volley.newRequestQueue(this);


    }

    @Override
    public int getItemCount() {
        return beaconsList.size();
    }


    public class BeaconViewHoldrer extends RecyclerView.ViewHolder{

        TextView textName, textDistance;

        public BeaconViewHoldrer(@NonNull View itemView) {
            super(itemView);
            textName = itemView.findViewById(R.id.textViewName);
            textDistance = itemView.findViewById(R.id.textDistance);

        }
    }
}
