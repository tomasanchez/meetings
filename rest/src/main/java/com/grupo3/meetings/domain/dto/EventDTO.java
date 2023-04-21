package com.grupo3.meetings.domain.dto;


import java.util.List;

public class EventDTO {

  List<OptionDTO> options;
  private String nombreDeEvento;
  private String descripcion;
  private String ubicacion;
  private String username;

  public EventDTO(String nombreDeEvento, String descripcion, String ubicacion, String userAdmin,
      List<OptionDTO> options) {
    this.nombreDeEvento = nombreDeEvento;
    this.descripcion = descripcion;
    this.ubicacion = ubicacion;
    this.username = userAdmin;
    this.options = options;
//        this.guests= new HashSet<>();
  }

  public EventDTO(String reunionDeDiscord) {
    this.nombreDeEvento = reunionDeDiscord;
  }

  public String getNombreDeEvento() {
    return nombreDeEvento;
  }

  public void setNombreDeEvento(String nombreDeEvento) {
    this.nombreDeEvento = nombreDeEvento;
  }

  public String getDescripcion() {
    return descripcion;
  }

  public void setDescripcion(String descripcion) {
    this.descripcion = descripcion;
  }

  public String getUbicacion() {
    return ubicacion;
  }

  public void setUbicacion(String ubicacion) {
    this.ubicacion = ubicacion;
  }

  public String getUsername() {
    return username;
  }

  public void setUsername(String username) {
    this.username = username;
  }


  public List<OptionDTO> getOptions() {
    return options;
  }

  public void setOptions(List<OptionDTO> options) {
    this.options = options;
  }

}
