package com.schedutn.scheduler.domain.models;


import java.io.Serializable;

/**
 * Base class for all entities.
 */
interface PersistentEntity extends Serializable {

  long serialVersionUID = 1L;

  /**
   * Obtains an unique identifier for the entity.
   *
   * @return the id of the entity.
   */
  String getIdentifier();

}
